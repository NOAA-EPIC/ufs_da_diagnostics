# UFS DA Diagnostics

`ufs_da_diagnostics` is a unified diagnostics toolkit for the UFS Data
Assimilation (DA) system. It provides consistent, experiment‑ready
diagnostics for analysis increments, spectral characteristics, and
observation‑space behavior. The tools are designed for FV3‑JEDI and the
broader UFS DA ecosystem, supporting research, tuning, verification, and
operational workflows.

The package contains three complementary diagnostics subsystems:

- **Increment diagnostics** — stitched global maps and zonal‑mean
  cross‑sections of analysis increments  
- **Spectral diagnostics** — 1D and 2D spectra, vertical variance
  profiles, and experiment‑difference spectral analysis  
- **Observation diagnostics** — statistics derived from both IODA files
  and JEDI logs, including counts, QC summaries, innovations (O–B, O–A),
  histograms, RMS/bias metrics, latitudinally binned statistics, and
  satellite‑specific checks such as ATMS scan‑position diagnostics

Each subsystem is driven by a YAML configuration and produces
standardized output directories suitable for experiment comparison,
documentation, and automated pipelines.

---

## Installation

```bash
pip install ufs_da_diagnostics
