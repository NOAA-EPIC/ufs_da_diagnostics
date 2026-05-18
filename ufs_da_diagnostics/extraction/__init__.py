"""
Extraction utilities for UFS DA Diagnostics.

This submodule provides tools for extracting subsets of observations
from IODA-formatted files, including single-observation extraction
for debugging, training, and experiment setup.
"""

from .single_obs import extract_single_obs, main

__all__ = [
    "extract_single_obs",
    "main",
]
