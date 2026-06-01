#!/usr/bin/env python3
"""
BKG–INC Spectral Diagnostics Driver
===================================

This script performs spectral diagnostics comparing **background fields**
against **analysis increments** for a single experiment. It is the backend
for the CLI entry point:

    ufsda-spectra-bkg-inc --yaml spectra_bkg_inc.yaml

The workflow:

1. Read YAML configuration
2. Load background fields from a single ATM file (all 6 tiles)
3. Load increment fields using ``SpectraCore`` (tile → global lat/lon)
4. Compute isotropic spectra for selected variables and levels
5. Generate comparison plots:
   - Background spectrum
   - Increment spectrum
   - Overlay plot (BKG + INC)
   - Annotated percentage contribution of increments

This driver uses:
- ``SpectraCore`` for increment processing
- Local helper functions for background loading and plotting
"""

import os
import sys
import yaml
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from scipy.interpolate import griddata

from .spectra_core import SpectraCore


# ---------------------------------------------------------
# Load background field (single ATM file, 6 tiles → global lat/lon)
# ---------------------------------------------------------
def load_bkg_field_global(atm_file, varname, level):
    """Load a background field from a single ATM file and regrid to lat/lon.

    Parameters
    ----------
    atm_file : str
        Path to the ATM background file containing all 6 tiles.
    varname : str
        Variable name inside the ATM file (e.g., ``"T"`` or ``"u"``).
    level : int
        Vertical level index.

    Returns
    -------
    numpy.ndarray
        2D field interpolated onto a regular global lat/lon grid.

    Notes
    -----
    - Background fields are stored as ``(tile, y, x)``.
    - All tiles are flattened and concatenated.
    - Regridding uses nearest-neighbor interpolation, matching
      ``SpectraCore.build_global``.
    """
    with Dataset(atm_file) as nc:
        lon = nc["lon"][:]   # (tile, grid_yt, grid_xt)
        lat = nc["lat"][:]   # (tile, grid_yt, grid_xt)

        fields = []
        lons = []
        lats = []

        for t in range(6):
            f_tile = nc[varname][0, t, level, :, :]
            fields.append(f_tile.flatten())
            lons.append(lon[t].flatten())
            lats.append(lat[t].flatten())

        field_global = np.concatenate(fields)
        lon_global   = np.concatenate(lons)
        lat_global   = np.concatenate(lats)

    lon_new = np.linspace(-180, 180, 360)
    lat_new = np.linspace(-90, 90, 181)
    Lon, Lat = np.meshgrid(lon_new, lat_new)

    field_interp = griddata(
        points=(lon_global, lat_global),
        values=field_global,
        xi=(Lon, Lat),
        method="nearest"
    )

    # subtract global mean (recommended for background spectra)
    field_interp = field_interp - np.nanmean(field_interp)

    return field_interp


# ---------------------------------------------------------
# Background: overlay bkg + inc + percentage text (boxed)
# ---------------------------------------------------------
def plot_bkg_overlay(k, Ek_bkg, Ek_inc, long_name, level, outname, pct_text):
    """Plot background and increment spectra with annotation.

    Parameters
    ----------
    k : numpy.ndarray
        Wavenumber array.
    Ek_bkg : numpy.ndarray
        Background isotropic spectrum.
    Ek_inc : numpy.ndarray
        Increment isotropic spectrum.
    long_name : str
        Human-readable variable name for plot title.
    level : int
        Vertical level index.
    outname : str
        Output PNG filename.
    pct_text : str
        Text describing increment percentage contribution.

    Notes
    -----
    The plot includes:
    - Background spectrum (black)
    - Increment spectrum (red)
    - Annotated DA contribution ranges
    """
    fig, ax = plt.subplots(figsize=(7, 5))

    ax.loglog(k, Ek_bkg, color="k", linewidth=1.5, label="Background")
    ax.loglog(k, Ek_inc, color="tab:red", linewidth=1.5, label="Increment")

    ax.set_title(
        f"{long_name} Isotropic Spectra — Background vs Increment (Level {level})"
    )

    ax.set_xlabel("Total wavenumber k")
    ax.set_ylabel("E(k)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()

    ax.text(
        0.02, 0.02,
        pct_text + "\n"
        "Expected DA contribution:\n"
        "  Large scales (k<10): 0.5–5%\n"
        "  Mid scales (10<k<40): 0.1–1%\n"
        "  Small scales (k>40): 0.01–0.1%",
        transform=ax.transAxes,
        fontsize=8,
        color="black",
        verticalalignment="bottom",
        bbox=dict(
            facecolor="white",
            edgecolor="black",
            boxstyle="round,pad=0.3",
            alpha=0.7
        )
    )

    fig.tight_layout()
    fig.savefig(outname, dpi=150)
    plt.close()


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def main():
    """Run BKG–INC spectral diagnostics from a YAML configuration file.

    This function implements the workflow for comparing background fields
    against analysis increments for a single experiment. It is invoked by
    the CLI entry point ``ufsda-spectra-bkg-inc``.

    YAML Configuration
    ------------------
    Expected structure:

    .. code-block:: yaml

        background:
          atm_file: "/path/to/atm_background.nc"

        increments:
          prefix: "/path/to/atminc.tile"
          grid_prefix: "/path/to/C96_grid.tile"

        mapping:
          - bkg: T
            inc: T_inc
            long_name: Temperature increment

        spectra:
          levels: [126, 75]
          output_dir: "./spectra_bkg_inc"

    Workflow
    --------
    1. Load background fields from a single ATM file
    2. Load increment fields using ``SpectraCore.build_global``
    3. Compute isotropic spectra for both fields
    4. Compute increment percentage contribution
    5. Generate overlay plots

    Returns
    -------
    None
        All output is written to PNG files in the configured output directory.
    """
    # --- YAML handling (supports --yaml or positional) ---
    if "--yaml" in sys.argv:
        idx = sys.argv.index("--yaml")
        yaml_file = sys.argv[idx + 1]
    else:
        yaml_file = sys.argv[1]

    with open(yaml_file) as f:
        cfg = yaml.safe_load(f)

    bkg_cfg = cfg["background"]
    inc_cfg = cfg["increments"]
    map_cfg = cfg["mapping"]
    spec_cfg = cfg["spectra"]

    atm_file = bkg_cfg["atm_file"]
    levels = spec_cfg["levels"]
    outdir = spec_cfg["output_dir"]
    os.makedirs(outdir, exist_ok=True)

    # SpectraCore instance for increments
    core = SpectraCore(grid_prefix=inc_cfg["grid_prefix"], suffix=".nc")

    for entry in map_cfg:
        bkg_name  = entry["bkg"]
        inc_name  = entry["inc"]
        long_name = entry.get("long_name", inc_name)

        core.varname = inc_name  # set increment variable

        for lev in levels:
            print(f"Processing {long_name} at level {lev}")

            # --- Background: single ATM file, 6 tiles → global ---
            bkg_field = load_bkg_field_global(atm_file, bkg_name, lev)
            spec_bkg = core.isotropic_spectrum(bkg_field)

            # --- Increment: 6 tiles via SpectraCore.build_global ---
            Lon, Lat, inc_field = core.build_global(inc_cfg["prefix"], lev)
            spec_inc = core.isotropic_spectrum(inc_field)

            k = np.arange(len(spec_bkg))

            # --- Percentage contribution ---
            percent = 100.0 * spec_inc / np.maximum(spec_bkg, 1e-12)
            pmin = np.nanmin(percent)
            pmax = np.nanmax(percent)
            pct_text = f"Increment contribution: {pmin:.3f}% – {pmax:.3f}%"

            # --- Background figure only ---
            outname_bkg = os.path.join(
                outdir, f"bkg_{inc_name}_L{lev}.png"
            )
            plot_bkg_overlay(k, spec_bkg, spec_inc, long_name, lev, outname_bkg, pct_text)

    print("Done.")


if __name__ == "__main__":
    main()

