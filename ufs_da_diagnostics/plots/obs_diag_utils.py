"""
obs_diag_utils.py — robust IODA-v2 loader with:
  • ATMS radiance support (InitialObsError)
  • GNSSRO fallback (no numeric ObsError)
  • SATWND/SCATWND vector wind support (windSpeed from u/v)
  • recursive group search for IODA-v2
  • compatibility with obs_diag_plotter YAML structure
"""

import os
import yaml
import numpy as np
from netCDF4 import Dataset

from .utils_loaders import (
    load_obsvalue,
    load_omb,
    load_oma_explicit,
    load_qc_universal,
)


# ---------------------------------------------------------------
# Recursive variable search in IODA-v2 groups
# ---------------------------------------------------------------
def find_variable_recursive(nc, varname):
    """Search for varname in root and all subgroups."""
    if varname in nc.variables:
        return nc.variables[varname][:]

    for gname, grp in nc.groups.items():
        if varname in grp.variables:
            return grp.variables[varname][:]
    return None


# ---------------------------------------------------------------
# Load a single diag file
# ---------------------------------------------------------------
def _load_single_instrument(diag_path, obsvar):
    if not os.path.exists(diag_path):
        raise FileNotFoundError(f"Diag file not found: {diag_path}")

    with Dataset(diag_path, "r") as f:

        # -------------------------------------------------------
        # Special case: vector winds (SATWND, SCATWND)
        # -------------------------------------------------------
        if obsvar == "windSpeed":
            u_name = "windEastward"
            v_name = "windNorthward"

            omb_u = load_omb(f, u_name)
            omb_v = load_omb(f, v_name)
            oma_u = load_oma_explicit(f, u_name)
            oma_v = load_oma_explicit(f, v_name)
            qc_u  = load_qc_universal(f, u_name)
            qc_v  = load_qc_universal(f, v_name)

            if omb_u is None or omb_v is None:
                raise RuntimeError(f"Missing wind components for SATWND/SCATWND in {diag_path}")

            # Wind-speed OMB/OMA
            omb = np.sqrt(omb_u**2 + omb_v**2)
            oma = np.sqrt(oma_u**2 + oma_v**2)

            # Combined QC
            qc = np.minimum(qc_u, qc_v)

            # No ObsError stored → fallback
            R_assumed = 1.0
            return omb, oma, qc, R_assumed

        # -------------------------------------------------------
        # Standard obs: load OMB / OMA / QC
        # -------------------------------------------------------
        obs = load_obsvalue(f, obsvar)
        omb = load_omb(f, obsvar)
        oma = load_oma_explicit(f, obsvar)
        qc  = load_qc_universal(f, obsvar)

        if omb is None:
            raise RuntimeError(f"Missing OMB for {obsvar} in {diag_path}")

        if oma is None:
            oma = np.zeros_like(omb)

        if qc is None:
            qc = np.zeros_like(omb, dtype=int)

        # -------------------------------------------------------
        # ObsError logic (robust IODA-v2 search)
        # -------------------------------------------------------

        # 0. Try obsvar-prefixed variants (GNSSRO, SATWND, SCATWND)
        prefixed_candidates = [
            f"{obsvar}@ObsError",
            f"{obsvar}@InitialObsError",
            f"{obsvar}@ObsErrorBound",
            f"{obsvar}@EffectiveError0",
            f"{obsvar}@EffectiveError1",
            f"{obsvar}@EffectiveError2",
        ]

        for name in prefixed_candidates:
            R = find_variable_recursive(f, name)
            if R is not None:
                if R.ndim == 2:
                    R_assumed = np.nanmean(R, axis=0)
                else:
                    R_assumed = R
                return omb, oma, qc, R_assumed

        # 1. Radiances: InitialObsError(Location, Channel)
        R = find_variable_recursive(f, "InitialObsError")
        if R is not None:
            if R.ndim == 2:
                R_assumed = np.nanmean(R, axis=0)
            else:
                R_assumed = R
            return omb, oma, qc, R_assumed

        # 2. Scalar obs: obsvar@ObsError (already covered above)

        # 3. Fallback error-like fields
        fallback_candidates = [
            "ObsErrorBound",
            "ObsErrorFactorLat",
            "ObsErrorFactorTopo",
            "ObsErrorFactorSurfJacobian",
            "ObsErrorFactorSituDepend",
            "ObsErrorFactorTransmitTop",
        ]

        for name in fallback_candidates:
            R = find_variable_recursive(f, name)
            if R is not None:
                if R.ndim == 2:
                    R_assumed = np.nanmean(R, axis=0)
                else:
                    R_assumed = R
                return omb, oma, qc, R_assumed

        # -------------------------------------------------------
        # FINAL FALLBACK — GNSSRO and others with NO numeric ObsError
        # -------------------------------------------------------

        if omb.ndim == 2:
            R_assumed = np.ones(omb.shape[1])   # per-channel fallback
        else:
            R_assumed = 1.0

        return omb, oma, qc, R_assumed


# ---------------------------------------------------------------
# Main loader for obs_diag.yaml
# ---------------------------------------------------------------
def load_obs_diag_data(yaml_path):

    with open(yaml_path, "r") as f:
        config = yaml.safe_load(f)

    prefix_root = config.get("prefix_root", "")
    obs_list = config.get("observations", [])

    data = {"omb": {}, "oma": {}, "qc": {}, "R": {}}

    for entry in obs_list:
        label  = entry["label"]
        obsvar = entry["variable"]

        diag_file = entry.get("diag", entry.get("file"))
        diag_path = os.path.join(prefix_root, diag_file)

        omb, oma, qc, R_assumed = _load_single_instrument(diag_path, obsvar)

        data["omb"][label] = omb
        data["oma"][label] = oma
        data["qc"][label]  = qc
        data["R"][label]   = R_assumed

    return data
