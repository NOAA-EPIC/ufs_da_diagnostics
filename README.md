# UFS DA Diagnostics

`ufs_da_diagnostics` is a diagnostics toolkit for FV3‑JEDI atmospheric
data assimilation (DA) experiments. It provides consistent,
experiment‑ready diagnostics for analysis increments, spectral
characteristics, and observation‑space behavior. The toolkit currently
supports the standard FV3‑JEDI canned case and includes observation
diagnostics for a limited set of five observation types:

- ASCAT MetOp‑B scatterometer winds (VertInterp)
- ATMS NOAA‑20 microwave radiances (CRTM)
- Surface pressure from SYNOP/METAR/ships/buoys (SfcCorrected)
- COSMIC‑2 GNSSRO bending angle (NBAM)
- GOES‑16 Atmospheric Motion Vectors (AMV operator)

While the present focus is FV3‑JEDI, the architecture is designed to
extend to additional UFS DA applications—including land and marine DA
systems—as those workflows mature and broader observation support becomes
available.

In progress [documentation](https://ufs-da-diagnostics.readthedocs.io/en/latest/) is available.

---

## Installation

```bash
git clone https://github.com/jkbk2004/ufs_da_diagnostics
cd ufs_da_diagnostics
pip install -e .
