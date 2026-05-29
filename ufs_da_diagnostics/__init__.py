"""
Unified import wrapper for UFS-DA diagnostics.

Provides top-level access to:
- plots: plotting utilities and diagnostic plotters
- increment: increment diagnostics and tile-based maps
- obs: observation diagnostics driver and utilities
- spectra: spectral analysis tools and drivers
- extraction: observation extraction utilities
- weather_events_marker: global weather feature diagnostics
"""

from . import plots
from . import increment
from . import obs
from . import spectra
from . import extraction
from . import weather_events_marker

__all__ = [
    "plots",
    "increment",
    "obs",
    "spectra",
    "extraction",
    "weather_events_marker",
]
