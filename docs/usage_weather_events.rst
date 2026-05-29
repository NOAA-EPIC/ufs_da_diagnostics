Weather Events Diagnostics
==========================

The ``ufsda-weather-events`` tool generates global synoptic‑scale
diagnostics from FV3 background files. It identifies cyclone centers,
jet streaks, and baroclinic zones using lightweight, reproducible
algorithms.

Running the Tool
----------------

.. code-block:: bash

   ufsda-weather-events <background_file.nc>

Example:

.. code-block:: bash

   ufsda-weather-events ufsda.t00z.atm.f006.cubed_sphere_grid.nc

This produces three PNG files:

* ``weather_cyclones_500.png``
* ``weather_jets_250.png``
* ``weather_baroclinic_850.png``

Inputs
------

The input file must contain:

* ``ugrd`` and ``vgrd`` on pressure levels
* ``tmp`` on pressure levels
* ``lat`` and ``lon`` coordinates
* ``pfull`` or ``lev`` pressure coordinate

Outputs
-------

Each diagnostic is plotted on a global 1°×1° lat/lon grid:

* **Cyclone Centers (500 hPa)** — smoothed vorticity + local maxima
* **Jet Streaks (250 hPa)** — wind‑speed ridges + contours
* **Baroclinic Zones (850 hPa)** — |∇T| magnitude + top‑10% mask

API Reference
-------------

See :doc:`api/weather_events_marker`.
