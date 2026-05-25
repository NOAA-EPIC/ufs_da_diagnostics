import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from netCDF4 import Dataset
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from .utils_loaders import (
    load_obsvalue,
    load_omb,
    load_oma_explicit,
    load_qc_universal,
)

from .atms_stats import plot_stats_atms
from .atms_stats_extended import plot_stats_atms_extended
from .atms_scan_position import plot_scan_position_atms
from .atms_latbins import plot_latbins_atms


# ============================================================
# Unified Histogram (ATMS, Scalar, Vector)
# ============================================================

def unified_histogram(omb, oma, qc, title_label, outpath, qc_label="QC", nbins=None):
    os.makedirs(os.path.dirname(outpath), exist_ok=True)

    omb = np.ravel(omb)
    oma = np.ravel(oma)
    qc  = np.ravel(qc)

    valid_omb = (qc == 0) & np.isfinite(omb)
    valid_oma = (qc == 0) & np.isfinite(oma)

    n_omb = int(np.sum(valid_omb))
    if n_omb == 0:
        print(f"[SKIP] {title_label}: no valid OMB")
        return

    if nbins is None:
        std = np.nanstd(omb[valid_omb])
        if np.isfinite(std) and std > 0:
            nbins = 100 if std < 1 else 80
        else:
            nbins = 50

    fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)

    ax.hist(
        omb[valid_omb],
        bins=nbins,
        color="lightgrey",
        edgecolor=None,
        alpha=0.7,
        density=True
    )

    if np.sum(valid_omb) > 1:
        sns.kdeplot(omb[valid_omb], color="dimgray", linewidth=2, ax=ax)
    if np.sum(valid_oma) > 1:
        sns.kdeplot(oma[valid_oma], color="red", linewidth=2, ax=ax)

    ax.set_xlabel("Value")
    ax.set_ylabel("Density")

    fig.text(
        0.12, 0.93,
        f"{title_label} ({qc_label}==0)",
        ha="left",
        fontsize=12
    )

    fig.text(
        0.18, 0.87,
        f"N assimilated = {n_omb}",
        ha="left",
        fontsize=9
    )

    ax.legend(
        handles=[
            plt.Line2D([0], [0], color="dimgray", lw=2, label="OMB"),
            plt.Line2D([0], [0], color="red", lw=2, label="OMA")
        ],
        loc="upper right",
        fontsize=8,
        frameon=False
    )

    if "GNSSRO" in title_label.upper():
        xmin, xmax = ax.get_xlim()
        center = 0.5 * (xmin + xmax)
        half = 0.5 * (xmax - xmin)
        ax.set_xlim(center - 0.2 * half, center + 0.2 * half)

    fig.savefig(outpath, dpi=150)
    plt.close(fig)
    print(f"[SAVED] {outpath}")


# ============================================================
# Main Orchestrator
# ============================================================

class ObsDiagPlotter:
    def __init__(self, config):
        self.config = config

        prefix_root = self.config.get("prefix_root", None)
        if prefix_root is not None:
            for obs in self.config.get("observations", []):
                if "file" in obs:
                    obs["diag"] = os.path.join(prefix_root, obs["file"])

    def run(self):
        obs_list = self.config.get("observations", [])

        global_outdir = (
            self.config.get("output_dir") or
            self.config.get("outdir") or
            "./plot-outputs-obs"
        )

        for obs_cfg in obs_list:
            label = obs_cfg["label"]
            otype = obs_cfg["type"]
            var = obs_cfg["variable"]

            diag = obs_cfg.get("diag", obs_cfg.get("file"))

            outdir = (
                obs_cfg.get("output_dir") or
                obs_cfg.get("outdir") or
                global_outdir
            )

            diags_cfg = obs_cfg.get("diagnostics", {})

            print(f"[INFO] Processing {label} ({otype}) from {diag}")
            with Dataset(diag, "r") as f:

                if otype == "atms":

                    if diags_cfg.get("hist", False):
                        self._plot_atms_histograms(f, var, label, outdir)

                    if diags_cfg.get("stats", False):
                        print(f"[INFO] Generating ATMS stats for {label}")
                        plot_stats_atms(f, var, label, outdir)

                    if diags_cfg.get("extended", False):
                        print(f"[INFO] Generating ATMS extended stats for {label}")
                        plot_stats_atms_extended(f, var, label, outdir)

                    if diags_cfg.get("scanpos", False):
                        print(f"[INFO] Generating ATMS scan-position diagnostics for {label}")
                        plot_scan_position_atms(f, var, label, outdir)

                    if diags_cfg.get("latbins", False):
                        print(f"[INFO] Generating ATMS latitude-binned diagnostics for {label}")
                        plot_latbins_atms(f, var, label, outdir)

                    if diags_cfg.get("scatter", False):
                        print(f"[INFO] Generating ATMS scatter for {label}")
                        self._plot_scatter(f, var, label, outdir)

                    if diags_cfg.get("scatter_map", False):
                        print(f"[INFO] Generating ATMS scatter map for {label}")
                        self._plot_scatter_map(f, var, label, outdir)

                elif otype == "scalar":
                    if diags_cfg.get("hist", False):
                        self._plot_scalar_hist(f, var, label, outdir)

                    if diags_cfg.get("scatter", False):
                        print(f"[INFO] Generating scalar scatter for {label}")
                        self._plot_scatter(f, var, label, outdir)

                    if diags_cfg.get("scatter_map", False):
                        print(f"[INFO] Generating scalar scatter map for {label}")
                        self._plot_scatter_map(f, var, label, outdir)

                elif otype == "vector":
                    if diags_cfg.get("hist", False):
                        self._plot_vector_hist(f, label, outdir)

                    if diags_cfg.get("scatter", False):
                        print(f"[INFO] Generating vector scatter for {label}")
                        self._plot_vector_scatter(f, label, outdir)

                    if diags_cfg.get("scatter_map", False):
                        print(f"[INFO] Generating vector scatter map for {label}")
                        self._plot_scatter_map_vector(f, label, outdir)

                else:
                    print(f"[WARN] Unknown type {otype} for {label}")

        print("[INFO] Diagnostics complete.")


    # ============================================================
    # ATMS Histograms
    # ============================================================

    def _plot_atms_histograms(self, f, varname, label, outdir):
        obs = load_obsvalue(f, varname)
        omb = load_omb(f, varname)
        oma = load_oma_explicit(f, varname)

        if obs is None or omb is None or oma is None:
            print(f"[SKIP] {label}: missing Obs/OMB/OMA")
            return

        qc = load_qc_universal(f, varname)
        if qc.ndim == 1:
            qc = np.repeat(qc[:, None], obs.shape[1], axis=1)

        nchan = obs.shape[1]
        for ch in range(nchan):
            ch_idx = ch + 1
            ch_label = f"{label} Ch {ch_idx:02d} Histogram"
            outpath = os.path.join(outdir, f"{label.lower()}_ch{ch_idx:02d}_hist.png")

            unified_histogram(
                omb[:, ch],
                oma[:, ch],
                qc[:, ch],
                ch_label,
                outpath,
                qc_label="QC2",
            )


    # ============================================================
    # Scalar Histograms
    # ============================================================

    def _plot_scalar_hist(self, f, varname, label, outdir):
        obs = load_obsvalue(f, varname)
        omb = load_omb(f, varname)
        oma = load_oma_explicit(f, varname)

        if obs is None and omb is None and oma is None:
            print(f"[SKIP] {label}: no Obs/OMB/OMA")
            return

        if omb is None:
            print(f"[INFO] {label}: No OMB found — using ObsValue only")
            omb = obs
        if oma is None:
            print(f"[INFO] {label}: No OMA found — using ObsValue only")
            oma = obs

        qc = load_qc_universal(f, varname)

        title_label = f"{label} Histogram"
        outpath = os.path.join(outdir, f"{label.lower()}_hist.png")

        unified_histogram(
            omb,
            oma,
            qc,
            title_label,
            outpath,
            qc_label="QC",
        )


    # ============================================================
    # Vector Histograms (U/V winds)
    # ============================================================

    def _plot_vector_hist(self, f, label, outdir):
        u_name = "windEastward"
        v_name = "windNorthward"

        omb_u = load_omb(f, u_name)
        oma_u = load_oma_explicit(f, u_name)
        omb_v = load_omb(f, v_name)
        oma_v = load_oma_explicit(f, v_name)

        if omb_u is None or oma_u is None or omb_v is None or oma_v is None:
            print(f"[SKIP] {label}: missing OMB/OMA for vector components")
            return

        qc_u = load_qc_universal(f, u_name)
        qc_v = load_qc_universal(f, v_name)

        unified_histogram(
            omb_u,
            oma_u,
            qc_u,
            f"{label} windEastward",
            os.path.join(outdir, f"{label.lower()}_u_hist.png"),
            qc_label="QC1",
        )

        unified_histogram(
            omb_v,
            oma_v,
            qc_v,
            f"{label} windNorthward",
            os.path.join(outdir, f"{label.lower()}_v_hist.png"),
            qc_label="QC1",
        )


    # ============================================================
    # Scatter Plot (ObsValue vs OMB) for scalar/ATMS
    # ============================================================

    def _plot_scatter(self, f, varname, label, outdir):
        obs = load_obsvalue(f, varname)
        omb = load_omb(f, varname)
        qc  = load_qc_universal(f, varname)

        if obs is None or omb is None:
            print(f"[SKIP] {label}: missing ObsValue or OMB")
            return

        valid = (qc == 0) & np.isfinite(obs) & np.isfinite(omb)
        if np.sum(valid) == 0:
            print(f"[SKIP] {label}: no assimilated points for scatter")
            return

        obs_valid = obs[valid]
        omb_valid = omb[valid]
        count = obs_valid.size

        scatter_dir = os.path.join(outdir, "scatter_plots")
        os.makedirs(scatter_dir, exist_ok=True)

        plt.figure(figsize=(6, 6))
        plt.scatter(obs_valid, omb_valid, s=2, alpha=0.4)
        plt.xlabel("ObsValue")
        plt.ylabel("OMB")
        plt.title(f"{label} (assimilated, count={count})")
        plt.grid(True)

        outfile = os.path.join(scatter_dir, f"{label.lower()}_omb_scatter.png")
        plt.savefig(outfile, dpi=150, bbox_inches="tight")
        plt.close()

        print(f"[SAVED] {outfile}")


    # ============================================================
    # Scatter Plot (ObsValue vs OMB) for vector winds
    # ============================================================

    def _plot_vector_scatter(self, f, label, outdir):
        u_name = "windEastward"
        v_name = "windNorthward"

        obs_u = load_obsvalue(f, u_name)
        obs_v = load_obsvalue(f, v_name)
        omb_u = load_omb(f, u_name)
        omb_v = load_omb(f, v_name)
        qc_u  = load_qc_universal(f, u_name)
        qc_v  = load_qc_universal(f, v_name)

        if obs_u is None or obs_v is None or omb_u is None or omb_v is None:
            print(f"[SKIP] {label}: missing U/V components for scatter")
            return

        obs_speed = np.sqrt(obs_u**2 + obs_v**2)

        omb_u = np.where(omb_u > 1e10, np.nan, omb_u)
        omb_v = np.where(omb_v > 1e10, np.nan, omb_v)
        omb_speed = np.sqrt(omb_u**2 + omb_v**2)

        qc = np.minimum(qc_u, qc_v)

        valid = (qc == 0) & np.isfinite(obs_speed) & np.isfinite(omb_speed)
        if np.sum(valid) == 0:
            print(f"[SKIP] {label}: no assimilated points for vector scatter")
            return

        obs_valid = obs_speed[valid]
        omb_valid = omb_speed[valid]
        count = obs_valid.size

        scatter_dir = os.path.join(outdir, "scatter_plots")
        os.makedirs(scatter_dir, exist_ok=True)

        plt.figure(figsize=(6, 6))
        plt.scatter(obs_valid, omb_valid, s=2, alpha=0.4)
        plt.xlabel("Obs wind speed")
        plt.ylabel("OMB wind speed")
        plt.title(f"{label} (assimilated, count={count})")
        plt.grid(True)

        outfile = os.path.join(scatter_dir, f"{label.lower()}_omb_scatter.png")
        plt.savefig(outfile, dpi=150, bbox_inches="tight")
        plt.close()

        print(f"[SAVED] {outfile}")


    # ============================================================
    # Global Map Scatter (scalar/ATMS)
    # ============================================================

    def _plot_scatter_map(self, f, varname, label, outdir):
        obs = load_obsvalue(f, varname)
        omb = load_omb(f, varname)
        qc  = load_qc_universal(f, varname)

        if obs is None or omb is None:
            print(f"[SKIP] {label}: missing ObsValue or OMB")
            return

        omb = np.where(omb > 1e10, np.nan, omb)

        if omb.ndim == 2:
            valid_rows = np.any(np.isfinite(omb), axis=1)
            omb_1d = np.full(omb.shape[0], np.nan)
            omb_1d[valid_rows] = np.nanmean(omb[valid_rows, :], axis=1)
            qc_1d = np.any(qc == 0, axis=1)
        else:
            omb_1d = omb
            qc_1d = (qc == 0)

        lat = lon = None

        if "MetaData" in f.groups:
            g = f.groups["MetaData"]
            if "latitude" in g.variables:
                lat = g.variables["latitude"][:]
            if "longitude" in g.variables:
                lon = g.variables["longitude"][:]

        if lat is None or lon is None:
            if "latitude" in f.variables and "longitude" in f.variables:
                lat = f.variables["latitude"][:]
                lon = f.variables["longitude"][:]

        if lat is None or lon is None:
            print(f"[SKIP] {label}: no latitude/longitude in file")
            return

        if lat.ndim == 2:
            lat = lat[:, 0]
        if lon.ndim == 2:
            lon = lon[:, 0]

        valid = qc_1d & np.isfinite(omb_1d) & np.isfinite(lat) & np.isfinite(lon)
        if np.sum(valid) == 0:
            print(f"[SKIP] {label}: no assimilated points for map")
            return

        lat = lat[valid]
        lon = lon[valid]
        omb = omb_1d[valid]
        N = len(lat)

        s = min(6.0, max(1.5, 30000 / N))

        if label.upper() == "GNSSRO":
            s = min(4.0, max(1.0, 50000 / N))
            alpha = 0.35
            vmin, vmax = np.percentile(omb, [0.5, 99.5])
        else:
            alpha = 0.7
            vmin, vmax = np.percentile(omb, [1, 99])

        map_dir = os.path.join(outdir, "scatter_maps")
        os.makedirs(map_dir, exist_ok=True)

        fig = plt.figure(figsize=(12, 6))
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.set_global()
        ax.coastlines()
        ax.add_feature(cfeature.BORDERS, linewidth=0.3)
        gl = ax.gridlines(draw_labels=True, linewidth=0.3)
        gl.top_labels = False
        gl.right_labels = False

        sc = ax.scatter(
            lon, lat,
            c=omb,
            s=s,
            alpha=alpha,
            cmap="coolwarm",
            linewidths=0,
            vmin=vmin, vmax=vmax,
            transform=ccrs.PlateCarree()
        )

        plt.colorbar(sc, ax=ax, label="OMB")
        plt.title(f"{label} (assimilated, count={N})")

        outfile = os.path.join(map_dir, f"{label.lower()}_omb_map.png")
        plt.savefig(outfile, dpi=150, bbox_inches="tight")
        plt.close()

        print(f"[SAVED] {outfile}")


    # ============================================================
    # Global Map Scatter (vector winds)
    # ============================================================

    def _plot_scatter_map_vector(self, f, label, outdir):
        u_name = "windEastward"
        v_name = "windNorthward"

        omb_u = load_omb(f, u_name)
        omb_v = load_omb(f, v_name)
        qc_u  = load_qc_universal(f, u_name)
        qc_v  = load_qc_universal(f, v_name)

        if omb_u is None or omb_v is None:
            print(f"[SKIP] {label}: missing U/V OMB components for map")
            return

        omb_u = np.where(omb_u > 1e10, np.nan, omb_u)
        omb_v = np.where(omb_v > 1e10, np.nan, omb_v)

        omb_speed = np.sqrt(omb_u**2 + omb_v**2)

        qc = np.minimum(qc_u, qc_v)
        qc_mask = (qc == 0)

        lat = lon = None
        if "MetaData" in f.groups:
            g = f.groups["MetaData"]
            if "latitude" in g.variables:
                lat = g.variables["latitude"][:]
            if "longitude" in g.variables:
                lon = g.variables["longitude"][:]

        if lat is None or lon is None:
            print(f"[SKIP] {label}: no latitude/longitude in file")
            return

        if lat.ndim == 2:
            lat = lat[:, 0]
        if lon.ndim == 2:
            lon = lon[:, 0]

        valid = qc_mask & np.isfinite(omb_speed) & np.isfinite(lat) & np.isfinite(lon)
        if np.sum(valid) == 0:
            print(f"[SKIP] {label}: no assimilated points for vector map")
            return

        lat = lat[valid]
        lon = lon[valid]
        omb = omb_speed[valid]
        N = len(lat)

        s = min(5.0, max(1.2, 25000 / N))
        alpha = 0.55

        vmin, vmax = np.percentile(omb, [2, 98])

        map_dir = os.path.join(outdir, "scatter_maps")
        os.makedirs(map_dir, exist_ok=True)

        fig = plt.figure(figsize=(12, 6))
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.set_global()
        ax.coastlines()
        ax.add_feature(cfeature.BORDERS, linewidth=0.3)
        gl = ax.gridlines(draw_labels=True, linewidth=0.3)
        gl.top_labels = False
        gl.right_labels = False

        sc = ax.scatter(
            lon, lat,
            c=omb,
            s=s,
            alpha=alpha,
            cmap="coolwarm",
            linewidths=0,
            vmin=vmin, vmax=vmax,
            transform=ccrs.PlateCarree()
        )

        plt.colorbar(sc, ax=ax, orientation="vertical", label="OMB wind speed")
        plt.title(f"{label} (assimilated, count={N})")

        outfile = os.path.join(map_dir, f"{label.lower()}_omb_map.png")
        plt.savefig(outfile, dpi=150, bbox_inches="tight")
        plt.close()

        print(f"[SAVED] {outfile}")
