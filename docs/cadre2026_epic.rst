CADRE 2026 EPIC Session Instructions
====================================

This page describes how to run the CADRE 2026 FV3-JEDI hybrid 3D-Var
training experiments on the Hercules HPC system and how to apply the
UFS DA Diagnostics toolkit to the resulting outputs. The three training
days focus on complementary aspects of hybrid 3D-Var data assimilation:

Day 1 — Control Experiment: System Access and Baseline Hybrid 3D-Var
    Establishes the baseline hybrid 3D-Var “control” experiment using the
    stand-alone FV3-JEDI job script on Hercules. Participants run the
    analysis end-to-end, verify outputs, and create a stable reference
    configuration for all subsequent sensitivity experiments.

Day 2 — Background Error Experiments: NICAS Length Scales and Hybrid Weights
    Focuses on SABER/BUMP background-error modeling. Participants modify
    NICAS horizontal length scales and adjust ensemble-static hybrid
    weights to examine how background-error parameters influence spatial
    correlations and analysis increments, comparing results against the
    Day 1 control.

Day 3 — Observation Error Experiments: ATMS Thinning and Error Tuning
    Explores observation-error modeling for ATMS radiances. Participants
    experiment with Gaussian thinning and ATMS observation-error
    inflation, evaluating impacts on QC decisions, innovation statistics,
    and overall analysis quality across all three days.

The Control Case
-----------------

The control case performs data assimilation for February 24, 2024. Globally, this date was signficant due to:

* Peak of a historically strong El Niño pattern
* Warmest February in recorded history
* Dissipation of Tropical Cyclone Eleanor in Mauritius 
* In the U.S.:

   * Winter cyclone swept snow into the Upper Midwest (Wisconsin & Michigan)
   * Record low ice cover over the Great Lakes
* Southern & Eastern Africa: Flash Floods vs. Intense Drought

Logging Into Hercules
---------------------

Use SSH with X11 forwarding enabled:

.. code-block:: bash

    ssh -X YOUR_USERID@hercules-login.hpc.msstate.edu

For detailed system login instructions (macOS/Windows, SSH, X11, PuTTY, XQuartz),
including screenshots and troubleshooting notes, see


- :ref:`Appendix A — System Access <appendix_system_access>`
- :ref:`Appendix B — Slurm Basics <appendix_slurm_basics>`
- :ref:`Appendix C — Filesystem and Modules <appendix_filesystem_modules>`

Clone the CADRE-DA-training Repository into Your EPIC Workspace
---------------------------------------------------------------

On Hercules, each user should clone the training repository inside their
EPIC project directory under ``/work2/noaa/epic-explorer/$USER``. This keeps the job
scripts, YAML files, and experiment outputs in the same workspace.

If you do not already have a directory in ``/work2/noaa/epic-explorer/``, you will need to create one: 

.. code-block:: bash

   mkdir -p /work2/noaa/epic-explorer/$USER

Then, navigate to your directory and clone the CADRE-DA-training repository:

.. code-block:: bash

    cd /work2/noaa/epic-explorer/$USER
    git clone https://github.com/NOAA-EPIC/CADRE-DA-training.git

Navigate to the ``year2_cases`` subdirectory in the repository and display its contents: 

.. code-block:: bash

    cd CADRE-DA-training/year2_cases
    ls

This directory includes the job card script (``run_3dvar_hercules.sh``) and input YAML files for the six experiments. 

.. code-block:: bash

   CADRE-DA-training/year2_cases
   ├── build_bundle.sh
   ├── build_gdas.sh
   ├── run_3dvar_hercules.sh
   └── input_yaml
       ├── Day1
       │   ├── jedi_3dvar_fv3_2024022400.yaml
       │   └── jedi_3dvar_fv3inc_2024022400.yaml
       ├── Day2
       │   ├── exp_hyb_weight
       │   │   ├── jedi_3dvar_fv3_2024022400.yaml
       │   │   └── jedi_3dvar_fv3inc_2024022400.yaml
       │   └── exp_nicas_scale
       │       ├── jedi_3dvar_fv3_2024022400.yaml
       │       └── jedi_3dvar_fv3inc_2024022400.yaml
       └── Day3
           ├── exp_gaussian_thinning
           │   ├── jedi_3dvar_fv3_2024022400.yaml
           │   └── jedi_3dvar_fv3inc_2024022400.yaml
           ├── exp_obs_error
           │   ├── jedi_3dvar_fv3_2024022400.yaml
           │   └── jedi_3dvar_fv3inc_2024022400.yaml
           └── exp_obs_options
               ├── jedi_3dvar_fv3_2024022400.yaml
               ├── jedi_3dvar_fv3_2024022400_3obs.yaml
               ├── jedi_3dvar_fv3_2024022400_4obs.yaml
               ├── jedi_3dvar_fv3_template.yaml
               ├── jedi_3dvar_fv3inc_2024022400.yaml
               ├── obs_ascat.yaml
               ├── obs_atms_n20.yaml
               ├── obs_conventional_ps.yaml
               ├── obs_gnssro_cosmic2.yaml
               └── obs_goes16.yaml

It also includes JEDI and GDAS build scripts; however, the FV3-JEDI and GDASApp executables are prebuilt on Hercules.

Running the CADRE 2026 Experiments
----------------------------------

The training experiments for Days 1-3 are executed using the
job card script located in the ``year2_cases`` directory. Copy the YAML configuration files for each day into your working
directory. For example, to copy the Day 1 YAMLs:

.. code-block:: bash

    cp ./input_yaml/Day1/*.yaml ./input_yaml

Each experiment contains two YAMLs: 

    #. ``jedi_3dvar_fv3_2024022400.yaml`` -- The FV3-JEDI input YAML
    #. ``jedi_3dvar_fv3inc_2024022400.yaml`` -- The GDASApp UFS increment-handling YAML 

Submit the job card using SLURM:

.. code-block:: bash

    sbatch run_3dvar_hercules.sh

Running this command will print a job ID, which should be retained for future reference. For example:

.. code-block:: bash

   Submitted batch job 8939236

Monitor job progress:

.. code-block:: bash

    squeue -u $USER

Prebuilt Experiment Outputs
---------------------------

All prebuilt CADRE 2026 experiment outputs are available at:

.. code-block:: text

    /work2/noaa/epic/CADRE2026

Example directory listing:

.. code-block:: text

    cadre26-diagnostics                      cadre26.8487557.day3_thinning
    cadre26.8434573.day1                     cadre26.8487565.day3_obs_error
    cadre26.8487509.day2_hyb_wght            cadre26.8697363_atms-err-08
    cadre26.8487556.day2_nicas               cadre26.8697429_atms-err-03
    cadre26.8487556.day2_nicas-length-scale  grid


Running Diagnostics After Jobs Complete
---------------------------------------

Once the FV3-JEDI jobs finish, the UFS DA Diagnostics toolkit can be
applied to the output files.

The diagnostics toolkit is installed at:

.. COMMENT: 
   Update path below so that it does not point to Jong

.. code-block:: text

    /work/noaa/epic/jongkim/ufs_da_diagnostics

Activate the Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^

To run the diagnostics package, first activate the preconfigured environment:

.. code-block:: bash

    export MPLBACKEND=Agg
    source /work/noaa/epic/jongkim/hercules.anaconda

Prepare Diagnostics YAML Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Optionally, save your epic-explorer directory in an environment variable:

.. code-block:: bash

   export HOME=/work2/noaa/epic-explorer/$USER

If you choose not to perform this step, you will need to type out the full path to your directory wherever it says ``$HOME``. 

Navigate to your experiment directory:

.. code-block:: console

   cd $HOME/CADRE-DA-training/year2_cases/exp_case

Diagnostics YAML templates for all CADRE 2026 training days are already
available under:

.. code-block:: text

    $HOME/CADRE-DA-training/diagnostics/yamls/day1
    $HOME/CADRE-DA-training/diagnostics/yamls/day2_hyb_weight
    $HOME/CADRE-DA-training/diagnostics/yamls/day2_nicas_length_scale
    $HOME/CADRE-DA-training/diagnostics/yamls/day3_atms_thining
    $HOME/CADRE-DA-training/diagnostics/yamls/day3_atms_err_03
    $HOME/CADRE-DA-training/diagnostics/yamls/day3_atms_err_08

Before running the diagnostics, edit the YAML files for the
corresponding day to set:

* the correct path to your experiment outputs (for example:
  ``$HOME/CADRE-DA-training/diag-results`` or your own experiment directory)
* the variables you want to diagnose (for example: T_inc, u_inc, v_inc)
* the output directory where figures and tables will be written

Typical fields to update inside each YAML include:

* Entries for ``diagnostics``, ``zonal_mean``, ``grid``,  ``mapping``, ``increments``, ``background``
* ``variable``, ``levels``, or ``vars`` list
* ``diag``, ``prefix``, ``outdir``, or ``output_dir``  

Day 1: Control Experiment Diagnostics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Navigate to the diagnostic YAMLs directory for Day 1: 

.. code-block:: bash

    cd $HOME/CADRE-DA-training/diagnostic/yamls/day1

Update data paths in each YAML to point to the location of your experiment output. 

Increment Plots
`````````````````

For the increment plots, open ``increment_maps.yaml``, and change the paths to point to your experiment directory output: 

.. code-block:: yaml

   vars:
     - T_inc
     - sphum_inc
     - u_inc
     - v_inc

   levels:
     - 126
     - 75

   zonal_mean:
   enabled: true
   full_vertical: true

   experiments:
     - name: ctrl
       prefix: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.8939236/output/ufsda.t00z.atminc.cubed_sphere_grid.tile"

   grid:
     prefix: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.8939236/grid/C96_grid.tile"

   output_dir: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.8939236/plots/inc_plots"

.. note:: 

   The script will not convert ``$USER`` or ``$HOME`` to their actual values, so users must type out the literal values in the path. Additionally, users will need to change the ``cadre26.8939236`` directory name to match their directory. 

Users may also choose to add or remove variables and levels, although this has not been tested. 

.. COMMENT: Check on above statement^

Then, run: 

.. code-block:: bash
   
    ufsda-inc-maps --yaml increment_maps.yaml

Observation Diagnostics
`````````````````````````

For the observation diagnostics plots, open ``obs_diag.yaml``. Change the ``output_dir`` path to point to a location where the plots will be stored, and change ``prefix_root`` to point to your experiment directory output:

.. code-block:: yaml

   output_dir: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.8939236/plots/obs-diag-plots"

   # Shared prefix for all diag files
   prefix_root: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.8939236/output"
   
   observations:

     # ------------------------------------------------------------
     # ATMS Radiances
     # ------------------------------------------------------------
     - label: ATMS
       type: atms
       variable: brightnessTemperature
       file: "diag.atms_n20_2024022400.nc"
       diagnostics:
         hist: true
         stats: true
         extended: true
         scanpos: true
         latbins: true
  
     ...

Then run:

.. code-block:: bash
   
    ufsda-obs-diag --yaml obs_diag.yaml

Power Spectra Analysis Plots
``````````````````````````````

For the power spectra analysis plots, adjust the file locations to point to your data. Users will need to change ``<username>`` to point to their actual username and also adjust the job ID: 

.. code-block:: yaml

   background:
     atm_file: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.8939236/bkg/ufsda.t18z.atm.f006.cubed_sphere_grid.nc"
     vars:
       - ugrd
       - vgrd
       - tmp
       - spfh

   increments:
     prefix: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.8939236/output/ufsda.t00z.atminc.cubed_sphere_grid.tile"
     grid_prefix: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.8939236/grid/C96_grid.tile"
     vars:
       - u_inc
       - v_inc
       - T_inc
       - sphum_inc

   ...

   spectra:
     levels:
       - 126
       - 75
     output_dir: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.8939236/plots/spectra-bkg-inc"

Then run: 

.. code-block:: bash
   
    ufsda-spectra-bkg-inc --yaml spectra_bkg_inc.yaml

JEDI Logs
```````````

To produce 

.. code-block:: bash
   
    ufsda-jedi-log /work2/noaa/epic-explorer/gpetro/CADRE-DA-training/year2_cases/exp_case/cadre26.8939236/OUTPUT.fv3jedi --output day1_log_report.txt

Day 2: Background Error Experiments (Hybrid Weight, NICAS)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    ufsda-spectra-ana-inc --yaml spectra_day2.yaml
    ufsda-inc-maps --yaml increment_maps_day2.yaml
    ufsda-obs-diag --yaml obs_diag_day2.yaml
    ufsda-jedi-log /work2/noaa/epic/CADRE2026/cadre26.8487509.day2_hyb_wght/OUTPUT.fv3jedi \
        --output day2_log_report.txt

Day 3: Observation Experiments (Thinning, Obs Error)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    ufsda-spectra-ana-inc --yaml spectra_day3.yaml
    ufsda-inc-maps --yaml increment_maps_day3.yaml
    ufsda-obs-diag --yaml obs_diag_day3.yaml
    ufsda-jedi-log /work2/noaa/epic/CADRE2026/cadre26.8487565.day3_obs_error/OUTPUT.fv3jedi \
        --output day3_log_report.txt

Notes
-----

* All YAML files referenced above should be copied from the CADRE-DA-training
  repository into your working input_yaml directory.
* The diagnostics output directories will be created automatically.
* Figures and tables generated by the diagnostics toolkit can be used
  directly in the CADRE 2026 training slides and documentation.
