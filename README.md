# UFS DA Diagnostics

`ufs_da_diagnostics` is a general diagnostics toolkit for the UFS Data Assimilation (DA) system. It provides consistent, experiment‑ready diagnostics for analysis increments, spectral characteristics, and observation‑space behavior. The tools currently support FV3‑JEDI and are being architected to extend naturally to additional UFS DA applications, including future land and marine data assimilation workflow systems.

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
git clone https://github.com/jkbk2004/ufs_da_diagnostics
cd ufs_da_diagnostics
pip install -e .
