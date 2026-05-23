Weather Events Diagnostics API
==============================

.. currentmodule:: ufs_da_diagnostics.weather_events_marker

The :mod:`ufs_da_diagnostics.weather_events_marker` module provides
global synoptic‑scale diagnostics derived from FV3 background fields.
It includes utilities for regridding, gradient computation, feature
detection, and global plotting.

This page documents the full API for programmatic use.

High‑Level Workflow
-------------------

The module performs the following steps:

* Build a regular 1°×1° lat/lon grid
* Regrid FV3 cubed‑sphere fields
* Compute:
  - wind speed
  - vorticity
  - temperature gradients
* Detect:
  - 500 hPa cyclone centers
  - 250 hPa jet streak ridges
  - 850 hPa baroclinic zones
* Produce global diagnostic plots

Functions
---------

Grid Utilities
~~~~~~~~~~~~~~

.. autofunction:: build_latlon_grid
.. autofunction:: flatten_fv3
.. autofunction:: regrid_fv3_to_latlon

Diagnostics
~~~~~~~~~~~

.. autofunction:: compute_vort_and_gradT
.. autofunction:: compute_gradT_only

Feature Detection
~~~~~~~~~~~~~~~~~

.. autofunction:: detect_jet_ridge
.. autofunction:: find_major_cyclone_centers

Plotting
~~~~~~~~

.. autofunction:: plot_map

Command‑Line Interface
----------------------

The module exposes a command‑line tool via:

.. code-block:: bash

   ufsda-weather-events <background_file.nc>

The CLI entry point calls:

.. autofunction:: main
