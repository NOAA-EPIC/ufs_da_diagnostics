CADRE 2026 EPIC Session Instructions
====================================

This page describes how to run the CADRE 2026 FV3-JEDI hybrid 3D-Var
training experiments on the Hercules HPC system and how to apply the
UFS-DA Diagnostics toolkit to the resulting outputs. The three training
days focus on complementary aspects of hybrid 3D-Var data assimilation:

Day 1 — Control Experiment: System Access and Baseline Hybrid 3D-Var
    Establishes the baseline hybrid 3D-Var “control” experiment using the
    stand-alone FV3-JEDI job script on Hercules. Participants run the
    analysis end-to-end, verify outputs, and create a stable reference
    configuration for all subsequent sensitivity experiments.

Day 2 — Background Error Experiments: NICAS Length Scales and Hybrid Weights
    Focuses on SABER/BUMP background-error modeling. Participants modify
    NICAS horizontal length scales and adjust ensemble–static hybrid
    weights to examine how background-error parameters influence spatial
    correlations and analysis increments, comparing results against the
    Day 1 control.

Day 3 — Observation Error Experiments: ATMS Thinning and Error Tuning
    Explores observation-error modeling for ATMS radiances. Participants
    experiment with Gaussian thinning and ATMS observation-error
    inflation, evaluating impacts on QC decisions, innovation statistics,
    and overall analysis quality across all three days.

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

Clone the CADRE-DA-training Repository into Your EPIC Workspace
---------------------------------------------------------------

On Hercules, each user should clone the training repository inside their
EPIC project directory under /work2/noaa/epic-explorer/$USER. This keeps the job
scripts, YAML files, and experiment outputs in the same workspace.

.. code-block:: bash

    mkdir -p /work2/noaa/epic-explorer/$USER
    cd /work2/noaa/epic-explorer/$USER
    git clone https://github.com/NOAA-EPIC/CADRE-DA-training.git
    cd CADRE-DA-training/year2_cases

Running the CADRE 2026 Experiments
----------------------------------

The FV3-JEDI and GDASApp executables are prebuilt on Hercules. The
training experiments for Day 1, Day 2, and Day 3 are executed using the
job card script:

.. code-block:: text

    run_3dvar_hercules.sh

Prebuilt Experiment Outputs
---------------------------

All prebuilt CADRE 2026 experiment outputs are available at:

.. code-block:: text

    /work2/noaa/epic-explorer/cadre2026

Example directory listing:

.. code-block:: text

    cadre26.8895896.day1_ctrl
    cadre26.8895942.day2_hyb_weight
    cadre26.8896455.day2_nicas_length_scale
    cadre26.8896479.day3_atms_thinning
    cadre26.8897035.day3_atms_err08
    cadre26.8900653.day3_no_atms
    cadre26.8900895.atms_err
    single_obs
    grid

Running Diagnostics After Jobs Complete
---------------------------------------

Once the FV3-JEDI jobs finish, the UFS-DA Diagnostics toolkit can be
applied to the output files. The following commands correspond to the
Quickstart examples, adapted for the CADRE 2026 experiment structure.

The diagnostics toolkit is installed and users can activate the preconfigured environment:

.. code-block:: bash

    export MPLBACKEND=Agg
    source /work/noaa/epic-explorer/cadre2026/hercules.anaconda

Prepare Diagnostics YAML Files
------------------------------

Diagnostics YAML templates for all CADRE 2026 training days are already
available under:

.. code-block:: text

    /path/to/CADRE-DA-training/diagnostics/yamls/day1
    /path/to/CADRE-DA-training/diagnostics/yamls/day2_hyb_weight
    /path/to/CADRE-DA-training/diagnostics/yamls/day2_nicas_length_scale
    /path/to/CADRE-DA-training/diagnostics/yamls/day3_atms_thining
    /path/to/CADRE-DA-training/diagnostics/yamls/day3_atms_err
    /path/to/CADRE-DA-training/diagnostics/yamls/day3_no_atms

Before running the diagnostics, edit the YAML files for the
corresponding day to set:

* the correct path to your experiment outputs (for example:
  /path/to/CADRE-DA-training/diag-results or your own experiment directory)
* the variables you want to diagnose (for example: T_inc, u_inc, v_inc)
* the output directory where figures and tables will be written

Typical fields to update inside each YAML include:

* ``diagnostics``, ``zonal_mean``, ``grid``,  ``mapping``, ``increments``, ``background``, entries
* ``variable``, ``levels``, or ``vars`` list
* ``diag``, ``prefix``, ``outdir``, or ``output_dir``  


Run the Day 1 Control Experiment and Diagnostics
------------------------------------------------

.. code-block:: bash

    cd /work2/noaa/epic-explorer/$USER/CADRE-DA-training/year2_cases
    cp ./input_yaml/Day1/*.yaml ./input_yaml
    sbatch run_3dvar_hercules.sh
    squeue -u $USER

.. code-block:: bash

    ufsda-spectra-ana-inc --yaml spectra_day1.yaml
    ufsda-inc-maps --yaml increment_maps_day1.yaml
    ufsda-obs-diag --yaml obs_diag_day1.yaml
    ufsda-jedi-log /work2/noaa/epic/CADRE2026/cadre26.8434573.day1/OUTPUT.fv3jedi \
        --output day1_log_report.txt

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
