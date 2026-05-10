Using Increment Diagnostics
===========================

The increment diagnostics subsystem generates FV3 6‑tile maps, stitched
global maps, and zonal‑mean summaries for analysis increments. These
diagnostics provide spatial insight into how the analysis modifies the
background state. For the mathematical formulation and example spectra,
see :ref:`Diagnostics Overview <diagnostics_overview>`.

Running the CLI Tool
--------------------

The main driver for increment diagnostics is:

.. code-block:: bash

    ufsda-inc-maps --yaml /path/to/increment_maps.yaml

This tool loads FV3 tiles, constructs global stitched fields, and
computes zonal‑mean cross sections for each variable and level specified
in the YAML file.


Example Figures
---------------

Background vs Increment Spectra
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: _static/images/spectra/bkg_T_inc_L75.png
   :width: 90%
   :align: center

   Background and increment spectra for temperature at model level 75.
   The increment spectrum shows how analysis updates redistribute
   variance across spatial scales relative to the background. Enhanced
   small‑scale variance indicates localized corrections, while reduced
   high‑wavenumber variance indicates smoother increments.


NICAS Length‑Scale Example
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: _static/images/spectra/T_inc_ctrl_vs_length-scale_spectra_L75.png
   :width: 90%
   :align: center

   Comparison of CTRL and NICAS length‑scale experiments for temperature
   increments at level 75. The NICAS experiment uses a larger horizontal
   correlation length scale in the SABER NICAS operator, broadening the
   background‑error correlations and shifting variance toward large
   scales.


YAML Configuration
------------------

A minimal YAML configuration for increment maps:

.. code-block:: yaml

    experiments:
      - name: EXP
        prefix: /path/to/exp/ufsda.t00z.atminc.cubed_sphere_grid.tile

    grid:
      prefix: /path/to/grid/C96_grid.tile

    output_dir: increment_maps/

    vars:
      - u_inc
      - v_inc
      - T_inc

    levels:
      - 126
      - 75


Outputs
-------

- ``global_maps/`` — stitched global maps for each variable and level  
- ``zonal_means/`` — zonal‑mean cross sections (latitude vs level)  

These outputs provide complementary spatial perspectives on the
structure and scale of analysis increments.
