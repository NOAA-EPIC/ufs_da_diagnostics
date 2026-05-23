#!/usr/bin/env python3
"""
Global Weather Diagnostics:
- 500 hPa cyclone centers (vorticity-based)
- 250 hPa jet streaks (ridge detection)
- 850 hPa baroclinic zones (temperature gradient)
"""

import argparse
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter


# ============================================================
# GRID + REGRID UTILITIES
# ============================================================

def build_latlon_grid(dlat=1.0, dlon=1.0):
    """
    Build a regular global lat/lon grid.

    Parameters
    ----------
    dlat, dlon : float
        Grid spacing in degrees.

    Returns
    -------
    Lon, Lat : 2D arrays
        Target longitude/latitude meshgrid.
    """
    lat = np.arange(-90, 90 + dlat, dlat)
    lon = np.arange(0, 360, dlon)
    Lon, Lat = np.meshgrid(lon, lat)
    return Lon, Lat


def flatten_fv3(ds_lev, varname):
    """
    Flatten FV3 cubed-sphere variable + lat/lon into 1D arrays.
    """
    var = ds_lev[varname].values
    lat = ds_lev["lat"].values
    lon = ds_lev["lon"].values
    return var.reshape(-1), lat.reshape(-1), lon.reshape(-1)


def regrid_fv3_to_latlon(ds_lev, varname, Lon_tgt, Lat_tgt):
    """
    Regrid FV3 cubed-sphere field to regular lat/lon using nearest neighbor.
    """
    flat_var, flat_lat, flat_lon = flatten_fv3(ds_lev, varname)
    return griddata(
        points=(flat_lon, flat_lat),
        values=flat_var,
        xi=(Lon_tgt, Lat_tgt),
        method="nearest"
    )


# ============================================================
# DIAGNOSTICS
# ============================================================

def compute_vort_and_gradT(Lon, Lat, U, V, T):
    """
    Compute:
    - wind speed
    - relative vorticity (radian-based gradient)
    - temperature gradient magnitude

    Notes
    -----
    Using radian-based gradients produces smoother,
    more visually interpretable synoptic-scale fields.
    """
    wspd = np.sqrt(U**2 + V**2)

    # Convert to radians for gradient scaling
    lon_rad = np.deg2rad(Lon)
    lat_rad = np.deg2rad(Lat)

    # Grid spacing in radians
    dlon = np.gradient(lon_rad, axis=1)
    dlat = np.gradient(lat_rad, axis=0)

    # Vorticity ζ = dV/dx − dU/dy
    dVdx = np.gradient(V, axis=1) / dlon
    dUdy = np.gradient(U, axis=0) / dlat
    vort = dVdx - dUdy

    # Temperature gradient magnitude
    dTdx = np.gradient(T, axis=1) / dlon
    dTdy = np.gradient(T, axis=0) / dlat
    gradT = np.sqrt(dTdx**2 + dTdy**2)

    return wspd, vort, gradT


def compute_gradT_only(Lon, Lat, T):
    """
    Compute |∇T| using radian-based gradients.
    """
    lon_rad = np.deg2rad(Lon)
    lat_rad = np.deg2rad(Lat)

    dlon = np.gradient(lon_rad, axis=1)
    dlat = np.gradient(lat_rad, axis=0)

    dTdx = np.gradient(T, axis=1) / dlon
    dTdy = np.gradient(T, axis=0) / dlat

    return np.sqrt(dTdx**2 + dTdy**2)


# ============================================================
# FEATURE DETECTION
# ============================================================

def detect_jet_ridge(wspd, threshold=45):
    """
    Detect local maxima in wind speed above a threshold.

    Parameters
    ----------
    wspd : 2D array
        Wind speed field.
    threshold : float
        Minimum wind speed to consider part of the jet.

    Returns
    -------
    ridge : 2D boolean array
        True where a local jet maximum is detected.
    """
    mask = wspd > threshold
    ridge = np.zeros_like(wspd, dtype=bool)

    ny, nx = wspd.shape
    for i in range(1, ny - 1):
        for j in range(1, nx - 1):
            if not mask[i, j]:
                continue
            window = wspd[i-1:i+2, j-1:j+2]
            if wspd[i, j] == np.max(window):
                ridge[i, j] = True
    return ridge


def find_major_cyclone_centers(vort, wspd, size=41):
    """
    Identify major cyclone centers using smoothed vorticity.

    Logic
    -----
    - Use a percentile threshold to avoid noise.
    - Require moderate wind speed (≥20 m/s).
    - Require local vorticity maximum in a (size x size) window.
    """
    ny, nx = vort.shape
    k = size // 2

    thresh = np.nanpercentile(vort, 90)

    centers_i, centers_j = [], []

    for i in range(k, ny - k):
        for j in range(k, nx - k):
            if vort[i, j] < thresh:
                continue
            if wspd[i, j] < 20:
                continue
            window = vort[i-k:i+k+1, j-k:j+k+1]
            if vort[i, j] == np.nanmax(window):
                centers_i.append(i)
                centers_j.append(j)

    return np.array(centers_i), np.array(centers_j)


# ============================================================
# PLOTTING
# ============================================================

def plot_map(Lon, Lat, field, title, outname,
             cmap="coolwarm", levels=20,
             annotate_func=None,
             cbar_label=None):
    """
    Generic global map plotter with:
    - filled contours
    - compact bottom colorbar
    - optional annotation callback
    """
    proj = ccrs.PlateCarree()
    fig = plt.figure(figsize=(12, 6))
    ax = plt.axes(projection=proj)
    ax.set_global()
    ax.coastlines(linewidth=0.8)
    ax.add_feature(cfeature.BORDERS, linewidth=0.4)

    cf = ax.contourf(Lon, Lat, field, levels, cmap=cmap,
                     transform=proj, alpha=0.9)

    # Compact bottom colorbar
    cax = fig.add_axes([0.20, 0.07, 0.6, 0.015])
    cbar = plt.colorbar(cf, cax=cax, orientation="horizontal")

    if cbar_label:
        cbar.set_label(cbar_label, fontsize=10)

    if annotate_func:
        annotate_func(ax)

    ax.set_title(title)
    plt.savefig(outname, dpi=150, bbox_inches="tight")
    plt.close()


# ============================================================
# MAIN WORKFLOW
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Global weather diagnostics: cyclone, jet, baroclinic."
    )
    parser.add_argument("bkg_file", help="FV3 background file")
    args = parser.parse_args()

    # Load dataset
    ds = xr.open_dataset(args.bkg_file)
    lev_name = "pfull" if "pfull" in ds.coords else "lev"

    # Build target grid
    Lon, Lat = build_latlon_grid(dlat=1.0, dlon=1.0)

    # --------------------------------------------------------
    # 1. CYCLONE CENTERS (500 hPa)
    # --------------------------------------------------------
    ds500 = ds.isel(time=0).sel({lev_name: 500}, method="nearest")
    U500 = regrid_fv3_to_latlon(ds500, "ugrd", Lon, Lat)
    V500 = regrid_fv3_to_latlon(ds500, "vgrd", Lon, Lat)
    T500 = regrid_fv3_to_latlon(ds500, "tmp",  Lon, Lat)

    wspd500, vort500, _ = compute_vort_and_gradT(Lon, Lat, U500, V500, T500)

    # Smooth vorticity for synoptic structure
    vort500_smooth = gaussian_filter(vort500, sigma=1.0)

    # Scale for visualization
    vort500_plot = vort500_smooth * 1e5

    # Detect cyclone centers
    ci, cj = find_major_cyclone_centers(vort500_smooth, wspd500)
    ci = ci.astype(int)
    cj = cj.astype(int)

    def annotate_cyclones(ax):
        """Plot cyclone centers as bold yellow X markers."""
        ax.scatter(
            Lon[ci, cj], Lat[ci, cj],   # FIXED: use ci,cj for BOTH Lon and Lat
            s=80,
            marker="X",
            color="yellow",
            edgecolor="black",
            linewidth=1.0,
            transform=ccrs.PlateCarree(),
            zorder=10
        )

    plot_map(
        Lon, Lat, vort500_plot,
        title="Major Cyclone Centers — 500 hPa Vorticity",
        outname="weather_cyclones_500.png",
        cmap="RdBu_r",
        levels=21,
        annotate_func=annotate_cyclones,
        cbar_label="Scaled Vorticity (×1e−5)"
    )

    # --------------------------------------------------------
    # 2. JET STREAKS (250 hPa)
    # --------------------------------------------------------
    ds250 = ds.isel(time=0).sel({lev_name: 250}, method="nearest")
    U250 = regrid_fv3_to_latlon(ds250, "ugrd", Lon, Lat)
    V250 = regrid_fv3_to_latlon(ds250, "vgrd", Lon, Lat)
    wspd250 = np.sqrt(U250**2 + V250**2)

    # Smooth wind for cleaner ridge detection
    wspd250_smooth = gaussian_filter(wspd250, sigma=1.0)
    ridge250 = detect_jet_ridge(wspd250_smooth)

    def annotate_jets(ax):
        """Plot jet contours + ridge line."""
        ax.contour(Lon, Lat, wspd250_smooth,
                   levels=[30, 40, 50, 60],
                   colors="white", linewidths=0.8,
                   transform=ccrs.PlateCarree())

        ax.contour(Lon, Lat, wspd250_smooth,
                   levels=[60],
                   colors="red", linewidths=1.2,
                   transform=ccrs.PlateCarree())

        # Ridge with black outline
        ax.contour(Lon, Lat, ridge250,
                   levels=[0.5],
                   colors="yellow", linewidths=2.5,
                   transform=ccrs.PlateCarree())
        ax.contour(Lon, Lat, ridge250,
                   levels=[0.5],
                   colors="black", linewidths=0.6,
                   transform=ccrs.PlateCarree())

    plot_map(
        Lon, Lat, wspd250_smooth,
        title="Jet Streaks — 250 hPa Wind Speed",
        outname="weather_jets_250.png",
        cmap="viridis",
        levels=20,
        annotate_func=annotate_jets,
        cbar_label="Wind Speed (m/s)"
    )

    # --------------------------------------------------------
    # 3. BAROCLINIC ZONES (850 hPa)
    # --------------------------------------------------------
    ds850 = ds.isel(time=0).sel({lev_name: 850}, method="nearest")
    T850 = regrid_fv3_to_latlon(ds850, "tmp", Lon, Lat)

    # Smooth temperature before gradient
    T850_smooth = gaussian_filter(T850, sigma=1.0)
    gradT850 = compute_gradT_only(Lon, Lat, T850_smooth)

    def annotate_baroclinic(ax):
        """Highlight strongest 10% of gradients."""
        bc_mask = gradT850 > np.nanpercentile(gradT850, 90)
        ax.contour(Lon, Lat, bc_mask,
                   levels=[0.5],
                   colors="cyan", linewidths=1.5,
                   transform=ccrs.PlateCarree())

    plot_map(
        Lon, Lat, gradT850,
        title="Baroclinic Zones — 850 hPa Temperature Gradient (Smoothed)",
        outname="weather_baroclinic_850.png",
        cmap="magma",
        levels=20,
        annotate_func=annotate_baroclinic,
        cbar_label="|∇T| (radian units)"
    )

    print("Saved: weather_cyclones_500.png")
    print("Saved: weather_jets_250.png")
    print("Saved: weather_baroclinic_850.png")


if __name__ == "__main__":
    main()
