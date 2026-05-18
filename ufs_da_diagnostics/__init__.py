"""
Unified import wrapper for UFS-DA diagnostics.

Provides top-level access to:
- plots: plotting utilities and diagnostic plotters
- increment: increment diagnostics and tile-based maps
- obs: observation diagnostics driver and utilities
- spectra: spectral analysis tools and drivers
- extraction: observation extraction utilities (e.g., single-observation extraction)
"""

from . import plots
from . import increment
from . import obs
from . import spectra
from . import extraction

__all__ = [
    "plots",
    "increment",
    "obs",
    "spectra",
    "extraction",
]
