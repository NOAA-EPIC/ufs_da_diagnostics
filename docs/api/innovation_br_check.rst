.. _api_innovation_br_check:

Innovation-Space Error Diagnostics API
======================================

This module implements the Desroziers innovation‑space diagnostic for
estimating observation‑error variance and background‑error contributions
using only the innovations (OMB and OMA). It is a lightweight tool for
monitoring the statistical consistency of the assumed observation-error
variance ``R`` in UFS DA workflows.

The diagnostic is implemented in:

``ufs_da_diagnostics/obs/innovation_br_check.py``

and is designed to operate on the same YAML configuration and data
structures used by the standard ``obs_diag`` utilities.

.. automodule:: ufs_da_diagnostics.obs.innovation_br_check
   :members:
   :undoc-members:
   :show-inheritance:
