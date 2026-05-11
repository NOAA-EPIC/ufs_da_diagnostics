Using Increment Diagnostics
===========================

The increment diagnostics subsystem generates FV3 6‑tile maps, stitched
global maps, and zonal‑mean summaries for analysis increments. These
diagnostics provide spatial insight into how the analysis modifies the
background state. They are complementary to observation‑space and
spectral diagnostics but do not compute spectra.

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

Global Increment Map
~~~~~~~~~~~~~~~~~~~~

.. figure:: _static/images/increments/sphum_inc_L126_ctrl.png
   :width: 90%
   :align: center

   Example stitched global increment map for specific humidity at
   model level 126. Positive increments indicate moistening applied
   by the analysis, while negative increments indicate drying.


Zonal‑Mean Increment Cross‑Section
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: _static/images/increments/sphum_inc_zonal_mean_full_ctrl.png
   :width: 90%
   :align: center

   Full‑vertical zonal‑mean increment cross‑section for specific
   humidity. This view highlights the vertical structure and
   latitudinal distribution of the analysis increments.


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
      - sphum_inc

    levels:
      - 126
      - 75


Outputs
-------

- ``global_maps/`` — stitched global maps for each variable and level  
- ``zonal_means/`` — zonal‑mean cross sections (latitude vs level)  

These outputs provide complementary spatial perspectives on the
structure and scale of analysis increments.
