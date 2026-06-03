"""
ATMS‑only innovation-based B/R diagnostics using OMB/OMA and obs_diag.yaml.

Outputs per channel:
  • Sd        = E[OMB^2]                     (innovation variance)
  • R_est     = E[OMA * OMB]                 (Desroziers estimate of R_true)
  • Sd/R      = Sd divided by assumed R      (chi-square proxy)
  • R_est/R   = R_est divided by assumed R   (variance scaling indicator)
  • HBH^T     = Sd - R_est                   (background error contribution)
  • HBH^T/R   = (Sd - R_est) / R             (background-to-observation ratio)
  • scale_R   = R_est / R                    (variance multiplier from Desroziers)
  • infl_chi  = sqrt((Sd/R) / chi_target)    (std-dev inflation to target chi^2)

Usage:
    ufsda-obs-br-check --yaml obs_diag.yaml
"""

import numpy as np
from ..plots.obs_diag_utils import load_obs_diag_data


# -------------------------------------------------------------
# Scalar Desroziers formulas
# -------------------------------------------------------------
def compute_scalar_desroziers(omb, oma):
    """
    Desroziers (2005) identities:

        Sd     = E[OMB^2]
        R_est  = E[OMA * OMB]

    Sd = HBH^T + R_true
    R_est ≈ R_true
    """
    Sd = np.mean(omb * omb)
    R_est = np.mean(oma * omb)
    return Sd, R_est


# -------------------------------------------------------------
# ATMS‑only diagnostic
# -------------------------------------------------------------
def diagnose_atms(inst, omb, oma, R_assumed, qc):
    print(f"\n=== Instrument: {inst} ===")

    nloc, nchans = omb.shape

    # ---------------------------------------------------------
    # JEDI‑consistent counting
    # ---------------------------------------------------------
    total_obs = nloc * nchans
    good_mask_ch = (qc == 0) if qc.ndim == 2 else (qc[:, None] == 0)
    n_good_total = int(np.sum(good_mask_ch))
    n_bad_total = total_obs - n_good_total

    print(f"  Total obs (loc×chan) : {total_obs}")
    print(f"  Assimilated (QC==0)  : {n_good_total}")
    print(f"  Rejected (QC!=0)     : {n_bad_total}")
    print(f"  Multi-channel instrument with {nchans} channels")

    # ---------------------------------------------------------
    # Diagnostic header
    # ---------------------------------------------------------
    print("\n=== Innovation-Space Diagnostics for ATMS Radiances ===")
    print("  Sd        = E[OMB^2]                     (innovation variance)")
    print("  R_est     = E[OMA * OMB]                 (Desroziers estimate of R_true)")
    print("  Sd/R      = Sd divided by assumed R      (chi-square proxy)")
    print("  R_est/R   = R_est divided by assumed R   (variance scaling indicator)")
    print("  HBH^T     = Sd - R_est                   (background error contribution)")
    print("  HBH^T/R   = (Sd - R_est) / R             (background-to-observation ratio)")
    print("  scale_R   = R_est / R                    (variance multiplier from Desroziers)")
    print("  infl_chi  = sqrt((Sd/R) / chi_target)    (std-dev inflation to target chi^2)")
    print("")

    chi_target = 0.8

    # ---------------------------------------------------------
    # Per‑channel diagnostics
    # ---------------------------------------------------------
    for ch in range(nchans):
        omb_ch_all = omb[:, ch]
        oma_ch_all = oma[:, ch]
        qc_ch_all  = qc[:, ch] if qc.ndim == 2 else qc

        valid = (qc_ch_all == 0) & np.isfinite(omb_ch_all) & np.isfinite(oma_ch_all)
        if np.sum(valid) < 5:
            print(f"  Ch {ch+1:02d}: too few valid obs")
            continue

        omb_ch = omb_ch_all[valid]
        oma_ch = oma_ch_all[valid]

        R0_ch = R_assumed[ch] if np.ndim(R_assumed) > 0 else R_assumed

        # Desroziers stats
        Sd, R_est = compute_scalar_desroziers(omb_ch, oma_ch)

        ratio_Sd_R   = Sd / R0_ch
        ratio_Rest_R = R_est / R0_ch

        # HBH^T and HBH^T/R
        HBHT = Sd - R_est
        HBHT_over_R = HBHT / R0_ch

        # Desroziers variance scaling
        scale_R = R_est / R0_ch

        # Chi-target scaling (variance) and inflation (std-dev)
        scale_R_chi = ratio_Sd_R / chi_target
        infl_chi = np.sqrt(scale_R_chi)

        print(
            f"  Ch {ch+1:02d}: "
            f"Sd/R={ratio_Sd_R:.3f}  "
            f"R_est/R={ratio_Rest_R:.3f}  "
            f"HBH^T={HBHT:.3f}  "
            f"HBH^T/R={HBHT_over_R:.3f}  "
            f"scale_R={scale_R:.3f}  "
            f"infl_chi={infl_chi:.3f}"
        )


# -------------------------------------------------------------
# Run diagnostics for ATMS only
# -------------------------------------------------------------
def run_br_check(yaml_path):
    data = load_obs_diag_data(yaml_path)

    print(f"Running ATMS‑only B/R diagnostics using: {yaml_path}")

    if "ATMS" not in data["omb"]:
        print("ERROR: No ATMS instrument found in obs_diag.yaml")
        return

    inst = "ATMS"
    diagnose_atms(
        inst,
        data["omb"][inst],
        data["oma"][inst],
        data["R"][inst],
        data["qc"][inst],
    )


# -------------------------------------------------------------
# CLI entry point
# -------------------------------------------------------------
def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="ATMS‑only innovation-based B/R diagnostics"
    )
    parser.add_argument("--yaml", required=True, help="Path to obs_diag.yaml")
    args = parser.parse_args()
    run_br_check(args.yaml)


if __name__ == "__main__":
    main()
