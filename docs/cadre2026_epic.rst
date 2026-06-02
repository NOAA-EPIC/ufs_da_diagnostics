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

Use SSH and verify environment:

.. code-block:: bash

    ssh -X YOUR_USERID@hercules-login.hpc.msstate.edu
    module load contrib noaatools
    saccount_params
    groups

For detailed system login instructions (macOS/Windows, SSH, X11, PuTTY, XQuartz),
including screenshots and troubleshooting notes, see


- :ref:`Appendix A — System Access <appendix_system_access>`
- :ref:`Appendix B — Slurm Basics <appendix_slurm_basics>`
- :ref:`Appendix C — Filesystem and Modules <appendix_filesystem_modules>`

Clone the CADRE-DA-training Repository
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

This directory includes the job card script (``run_3dvar_hercules.sh``) and input YAML files for the six experiments and additional single_obs experiments. 

.. code-block:: bash

   CADRE-DA-training/year2_cases
   ├── build_bundle.sh
   ├── build_gdas.sh
   ├── run_3dvar_hercules.sh
   ├── input_yaml
   │   ├── Day1
   │   │   ├── jedi_3dvar_fv3_2024022400.yaml
   │   │   └── jedi_3dvar_fv3inc_2024022400.yaml
   │   ├── Day2
   │   │   ├── exp_hyb_weight
   │   │   │   ├── jedi_3dvar_fv3_2024022400.yaml
   │   │   │   └── jedi_3dvar_fv3inc_2024022400.yaml
   │   │   └── exp_nicas_scale
   │   │       ├── jedi_3dvar_fv3_2024022400.yaml
   │   │       └── jedi_3dvar_fv3inc_2024022400.yaml
   │   ├── Day3
   │   │   ├── exp_atm_thinning
   │   │   │   ├── jedi_3dvar_fv3_2024022400.yaml
   │   │   │   └── jedi_3dvar_fv3inc_2024022400.yaml
   │   │   ├── exp_atms_err
   │   │   │   ├── jedi_3dvar_fv3_2024022400.yaml
   │   │   │   └── jedi_3dvar_fv3inc_2024022400.yaml
   │   │   └── exp_no_atms
   │   │       ├── jedi_3dvar_fv3_2024022400.yaml
   │   │       └── jedi_3dvar_fv3inc_2024022400.yaml
   │   └── single_obs
   │       ├── atms_err
   │       │   ├── jedi_3dvar_fv3_2024022400.yaml
   │       │   └── jedi_3dvar_fv3inc_2024022400.yaml
   │       ├── ctrl
   │       │   ├── jedi_3dvar_fv3_2024022400.yaml
   │       │   └── jedi_3dvar_fv3inc_2024022400.yaml
   │       ├── hyb_weight
   │       │   ├── jedi_3dvar_fv3_2024022400.yaml
   │       │   └── jedi_3dvar_fv3inc_2024022400.yaml
   │       └── nicas_length_scale
   │           ├── jedi_3dvar_fv3_2024022400.yaml
   │           └── jedi_3dvar_fv3inc_2024022400.yaml
   └── year2_aws_setup
       ├── build_da_cluster.pkr.hcl
       ├── da-cluster-start-script.sh
       └── da_hpc.yaml

It also includes JEDI and GDAS build scripts; however, the FV3-JEDI and GDASApp executables are prebuilt on Hercules.

Each training experiment for Days 1-3 includes two YAML configuration files: 

    #. ``jedi_3dvar_fv3_2024022400.yaml`` -- The FV3-JEDI input YAML
    #. ``jedi_3dvar_fv3inc_2024022400.yaml`` -- The GDASApp UFS increment-handling YAML 

Day 1: Running the CADRE 2026 Control Experiment & Diagnostics
----------------------------------------------------------------

Running the Experiment
^^^^^^^^^^^^^^^^^^^^^^^^

To run the Day 1 control experiment, copy the Day 1 YAMLs to the ``year2_cases`` directory:

.. code-block:: bash

    cp ./input_yaml/Day1/*.yaml ./input_yaml

Each experiment contains two YAMLs: 

    #. ``jedi_3dvar_fv3_2024022400.yaml`` -- The FV3-JEDI input YAML
    #. ``jedi_3dvar_fv3inc_2024022400.yaml`` -- The GDASApp UFS increment-handling YAML 

Submit the job card using SLURM:

.. include:: code-snippets/submit-job.rst

Running this command will print a job ID, which should be retained for future reference. For example:

.. code-block:: bash

   Submitted batch job 8939236

Monitor job progress:

.. include:: code-snippets/monitor-job.rst

After the experiment has finished running, it can be helpful to rename the directory to something more descriptive. For example:

.. code-block:: bash

   cd exp_case
   mv cadre26.8939236 cadre26.control

Prebuilt Experiment Outputs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All prebuilt CADRE 2026 experiment outputs are available at:

.. code-block:: text

   /work2/noaa/epic-explorer/cadre2026

Example directory listing:

.. code-block:: text

   cadre26.8895896.day1_ctrl                 cadre26.8900895.atms_err
   cadre26.8895942.day2_hyb_weight           grid
   cadre26.8896455.day2_nicas_length_scale   hercules.anaconda
   cadre26.8896479.day3_atms_thinning        input_data
   cadre26.8897035.day3_atms_err08           single_obs
   cadre26.8900653.day3_no_atms


Running Diagnostics After Jobs Complete
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once the FV3-JEDI jobs finish, the UFS DA Diagnostics toolkit can be
applied to the output files.

The diagnostics toolkit is installed at:

.. code-block:: text

   /work2/noaa/epic-explorer/cadre2026/hercules.anaconda

Activate the Environment
``````````````````````````

To run the diagnostics package, first activate the preconfigured environment:

.. include:: code-snippets/activate-env.rst

Prepare Diagnostics YAML Files
````````````````````````````````

Optionally, save your epic-explorer directory in an environment variable:

.. include:: code-snippets/set-HOME.rst

If you choose not to perform this step, you will need to type out the full path to your directory wherever it says ``$HOME``. 

Diagnostics YAML templates for all CADRE 2026 training days are already
available under:

.. code-block:: text

    $HOME/CADRE-DA-training/diagnostics/yamls/day1
    $HOME/CADRE-DA-training/diagnostics/yamls/day2_hyb_weight
    $HOME/CADRE-DA-training/diagnostics/yamls/day2_nicas_length_scale
    $HOME/CADRE-DA-training/diagnostics/yamls/day3_atms_thining
    $HOME/CADRE-DA-training/diagnostics/yamls/day3_atms_err
    $HOME/CADRE-DA-training/diagnostics/yamls/day3_no_atms

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
```````````````````````````````````````

Navigate to the diagnostic YAMLs directory for Day 1: 

.. code-block:: bash

    cd $HOME/CADRE-DA-training/diagnostic/yamls/day1

Update data paths in each YAML to point to the location of your experiment output. 

Increment Plots
"""""""""""""""""

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
       prefix: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.control/output/ufsda.t00z.atminc.cubed_sphere_grid.tile"

   grid:
     prefix: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.control/grid/C96_grid.tile"

   output_dir: "./plots/inc_plots"

   amplify:
     enabled: false
     factor: 8.0
     apply_to_diff: false

.. note:: 

   The script will not convert ``$USER`` or ``$HOME`` to their actual values, so users must type out the literal values in the path. Additionally, users will need to change the ``cadre26.8939236`` directory name to match their directory. 

Then, run the following command to generate the plots: 

.. code-block:: bash
   
    ufsda-inc-maps --yaml increment_maps.yaml

Observation Diagnostics
"""""""""""""""""""""""""

For the observation diagnostics plots, open ``obs_diag.yaml``. Change the ``output_dir`` path to point to a location where the plots will be stored, and change ``prefix_root`` to point to your experiment directory output:

.. code-block:: yaml

   output_dir: "./plots/obs-diag"

   # Shared prefix for all diag files
   prefix_root: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.control/output"
   
   observations:

     # ------------------------------------------------------------
     # ATMS Radiances
     # ------------------------------------------------------------
     - label: ATMS
       type: atms
       variable: brightnessTemperature
       file: "diag.atms_n20_2024022400.nc"
     ...

Then, run the following command to generate the plots: 

.. code-block:: bash
   
    ufsda-obs-diag --yaml obs_diag.yaml

Power Spectra Analysis Plots
"""""""""""""""""""""""""""""

For the power spectra analysis plots, adjust the file locations to point to your data. Users will need to change ``<username>`` to point to their actual username and also adjust the job ID: 

.. code-block:: yaml

   background:
     atm_file: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.control/bkg/ufsda.t18z.atm.f006.cubed_sphere_grid.nc"
     vars:
       - ugrd
       - vgrd
       - tmp
       - spfh

   increments:
     prefix: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.control/output/ufsda.t00z.atminc.cubed_sphere_grid.tile"
     grid_prefix: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.control/grid/C96_grid.tile"
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
     output_dir: "./plots/spectra-bkg-inc"

Then, run the following command to generate the plots: 

.. code-block:: bash
   
    ufsda-spectra-bkg-inc --yaml spectra_bkg_inc.yaml

JEDI Logs
"""""""""""

To produce a JEDI DA summary diagnostics report, run the ``ufsda-jedi-log``

.. code-block:: bash
   
    ufsda-jedi-log $HOME/CADRE-DA-training/year2_cases/exp_case/cadre26.control/OUTPUT.fv3jedi --output ./day1_log_report.txt

Download Plots
""""""""""""""""

To download the plots onto the local system for viewing, users can run the ``scp`` command in a new terminal window: 

.. code-block:: bash

   scp -r <username>@hercules-login.hpc.msstate.edu:/work2/noaa/epic-explorer/<username>/CADRE-DA-training/diagnostic/yamls/day1/plots/*/*.png ./plots

Key Aspects to Verify Day 1 Experiment Outputs
----------------------------------------------

- Increment maps: smooth, physically consistent
- Zonal-mean increments: balanced vertical structure
- OMB/OMA: OMA variance < OMB variance
- Jo convergence: decreasing cost function
- Jo/p:reasonal range 
- Baseline power spectra: correct scale separation

Optional Single-Obs Experiments
-------------------------------

Single-observation YAMLs are available under:

.. code-block:: text

    CADRE-DA-training/year2_cases/input_yaml/single_obs

These include input yaml file directories for control, NICAS length-scale, hybrid-weight, and ATMS obs-error cases.

To run:

.. code-block:: bash

    cd /work2/noaa/epic-explorer/$USER/CADRE-DA-training/year2_cases
    cp ./input_yaml/single_obs/<case>/*.yaml ./input_yaml
    sbatch run_3dvar_hercules.sh

Diagnostics can be applied the same way as above.

Day 2: Background Error Experiments (Hybrid Weight, NICAS)
------------------------------------------------------------

The procedure for running Day 2 experiments and diagnostics is the same as for Day 1. Optionally, set your home directory to shorten the paths you type out: 

.. include:: code-snippets/set-HOME.rst

Then, navigate to the ``year2_cases`` directory and copy the experiment YAML file to the ``input_yaml`` directory: 

.. code-block:: bash

   cd $HOME/CADRE-DA-training/year2_cases
   cp ./input_yaml/Day2/<exp_name>/*.yaml ./input_yaml
   sbatch run_3dvar_hercules.sh

where ``<exp_name>`` is either ``exp_hyb_weight`` or ``exp_nicas_scale``. 

Monitor your results: 

.. include:: code-snippets/monitor-job.rst

If desired, rename your experiment directory when the experiment finishes running. For example: 

.. code-block:: bash

   cd exp_case
   mv cadre26.8972359 cadre26.hyb_weight
   # OR
   mv cadre26.8972360 cadre26.nicas_scale

To run the diagnostics package, first activate the preconfigured environment:

.. include:: code-snippets/activate-env.rst

Then, navigate to the diagnostics YAMLs, and adjust the data paths in each YAML to match the data input and output locations for your experiment. 

.. code-block:: bash

   cd $HOME/CADRE-DA-training/diagnostic/yamls/day2_<exp_name>

where ``<exp_name>`` is ``hyb_weight`` or ``nicas_scale``.

For example, to generate the hybrid weight increment plots, change the experiment paths in ``increment_maps.yaml`` to point to your experiment output: 

.. code-block:: yaml
   
   ...
   experiments:
     - name: ctrl
       prefix: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.control/output/ufsda.t00z.atminc.cubed_sphere_grid.tile"

     - name: atms-thining
       prefix: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.<exp_name>/output/ufsda.t00z.atminc.cubed_sphere_grid.tile"

   grid:
     prefix: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.<exp_name>/grid/C96_grid.tile"

   output_dir: "./plots/inc_plots"
   ...

Then, to generate the observation diagnostics plots, update the ``obs_diag.yaml`` file: 

.. code-block:: yaml

   output_dir: "./plots/obs-diag"

   # Shared prefix for all diag files
   prefix_root: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.<exp_name>/output"

   observations:

     # ------------------------------------------------------------
     # ATMS Radiances
     # ------------------------------------------------------------
     - label: ATMS
       type: atms
       variable: brightnessTemperature
       file: "diag.atms_n20_2024022400.nc"
       ...

To generate the power spectra analysis plots: 

.. code-block:: yaml

   experiments:
     - name: ctrl
       prefix: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.control/output/ufsda.t00z.atminc.cubed_sphere_grid.tile"

     - name: atms-thining
       prefix: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.<exp_name>/output/ufsda.t00z.atminc.cubed_sphere_grid.tile"

   grid:
     prefix: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.<exp_name>/grid/C96_grid.tile"

   output_dir: "./plots/spectra-inc"


Run the diagnostics package to generate the plots for the experiment:

.. code-block:: bash

    ufsda-spectra-ana-inc --yaml spectra_ana_inc.yaml
    ufsda-inc-maps --yaml increment_maps.yaml
    ufsda-obs-diag --yaml obs_diag.yaml
    ufsda-jedi-log /work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.<exp_name>/OUTPUT.fv3jedi \
        --output <exp_name>_log_report.txt

To download the plots onto the local system for viewing, users can run the ``scp`` command in a new terminal window: 

.. code-block:: bash

   scp -r <username>@hercules-login.hpc.msstate.edu:/work2/noaa/epic-explorer/<username>/CADRE-DA-training/diagnostic/yamls/day2_<exp_name>/plots/*/*.png ./plots

Day 3: Observation Experiments (Thinning, Obs Error)
-----------------------------------------------------

The procedure for running Day 3 experiments and diagnostics is the same as for Day 1. Optionally, set your home directory to shorten the paths you type out: 

.. include:: code-snippets/set-HOME.rst

Then, navigate to the ``year2_cases`` directory and copy the experiment YAML file to the ``input_yaml`` directory: 

.. code-block:: bash

   cd $HOME/CADRE-DA-training/year2_cases
   cp ./input_yaml/Day3/<exp_name>/*.yaml ./input_yaml
   sbatch run_3dvar_hercules.sh

where ``<exp_name>`` is ``exp_atm_thinning``, ``exp_atms_err``, or ``exp_no_atms``. 

Monitor your results: 

.. include:: code-snippets/monitor-job.rst

If desired, rename your experiment directory when the experiment finishes running. For example: 

.. code-block:: bash

   cd exp_case
   mv cadre26.8978018 cadre26.atm_thinning
   # OR
   mv cadre26.8978027 cadre26.atms_err
   # OR
   mv cadre26.8978028 cadre26.no_atms

To run the diagnostics package, first activate the preconfigured environment:

.. include:: code-snippets/activate-env.rst

Then, navigate to the diagnostics YAMLs, and adjust the data paths in each YAML to match the data input and output locations for your experiment. 

.. code-block:: bash

   cd $HOME/CADRE-DA-training/diagnostic/yamls/day3_<exp_name>

where ``<exp_name>`` is ``atm_thinning``, ``atms_err``, or ``no_atms``. 

For example, to generate the hybrid weight increment plots, change the experiment paths in ``increment_maps.yaml`` to point to your experiment output: 

.. code-block:: yaml
   
   ...
   experiments:
     - name: ctrl
       prefix: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.control/output/ufsda.t00z.atminc.cubed_sphere_grid.tile"

     - name: atms-thining
       prefix: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.<exp_name>/output/ufsda.t00z.atminc.cubed_sphere_grid.tile"

   grid:
     prefix: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.<exp_name>/grid/C96_grid.tile"

   output_dir: "./plots/inc_plots"
   ...

Then, to generate the observation diagnostics plots, update the ``obs_diag.yaml`` file: 

.. code-block:: yaml

   output_dir: "./plots/obs-diag"

   # Shared prefix for all diag files
   prefix_root: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.<exp_name>/output"

   observations:

     # ------------------------------------------------------------
     # ATMS Radiances
     # ------------------------------------------------------------
     - label: ATMS
       type: atms
       variable: brightnessTemperature
       file: "diag.atms_n20_2024022400.nc"
       ...

To generate the power spectra analysis plots: 

.. code-block:: yaml

   experiments:
     - name: ctrl
       prefix: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.control/output/ufsda.t00z.atminc.cubed_sphere_grid.tile"

     - name: atms-thining
       prefix: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.<exp_name>/output/ufsda.t00z.atminc.cubed_sphere_grid.tile"

   grid:
     prefix: "/work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.<exp_name>/grid/C96_grid.tile"

   output_dir: "./plots/spectra-inc"

.. code-block:: bash

    ufsda-spectra-ana-inc --yaml spectra_ana_inc.yaml
    ufsda-inc-maps --yaml increment_maps.yaml
    ufsda-obs-diag --yaml obs_diag.yaml
    ufsda-jedi-log /work2/noaa/epic-explorer/<username>/CADRE-DA-training/year2_cases/exp_case/cadre26.<exp_name>/OUTPUT.fv3jedi \
        --output day3_log_report.txt

To download the plots onto the local system for viewing, users can run the ``scp`` command in a new terminal window: 

.. code-block:: bash

   scp -r <username>@hercules-login.hpc.msstate.edu:/work2/noaa/epic-explorer/<username>/CADRE-DA-training/diagnostic/yamls/day3_<exp_name>/plots/*/*.png ./plots

Notes
-----

* All YAML files referenced above can be copied from the CADRE-DA-training
  repository into your working ``input_yaml`` directory instead.
* The diagnostics output directories will be created automatically.
* Figures and tables generated by the diagnostics toolkit can be used
  directly in the CADRE 2026 training slides and documentation.
