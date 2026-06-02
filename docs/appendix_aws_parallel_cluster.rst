===========================================================
NOAA AWS Parallel Cluster — CADRE 2026 Workshop Instructions
===========================================================

SSH Setup, JEDI Execution, Diagnostics, and File Download
=========================================================

SSH Key Generation
------------------

A Secure SHell (SSH) tunnel creates an encrypted connection between two systems.
Many HPC platforms, including NOAA systems and commercial cloud systems (AWS, Azure),
are accessed via SSH.

Instructions for Mac Users
--------------------------

Generate a public/private key pair:

.. code-block:: bash

    ssh-keygen -t ed25519 -f /Users/<username>/.ssh/id_ed25519_student{1-30}

Leave the passphrase empty (press Enter twice).

View your public key:

.. code-block:: bash

    vim /Users/<username>/.ssh/id_ed25519_student(n).pub

Send **only** the ``.pub`` file to the workshop admin via Slack
(``#cadre-epic-data-assimilation-training``).

Add the key to your SSH agent:

.. code-block:: bash

    ssh-add /Users/<username>/.ssh/id_ed25519_student(n)

Log in to the HPC environment:

.. code-block:: bash

    ssh student(n)@137.75.93.46


Instructions for Windows Users
------------------------------

Generate keys:

.. code-block:: powershell

    ssh-keygen -t ecdsa

Leave the passphrase empty.

View the public key:

.. code-block:: powershell

    type C:\Users\<username>\.ssh\id_ecdsa.pub

Send the ``.pub`` file to the workshop admin.

Connect to the HPC environment:

.. code-block:: powershell

    ssh -i C:\Users\<username>\.ssh\id_ecdsa student(n)@137.75.93.46


Run JEDI (FV3-JEDI)
===================

If you already set up the repository and input dataset on Day 1, skip steps 1–4.

Clone the repository:

.. code-block:: bash

    git clone https://github.com/chan-hoo/cadre26_noaa_tutorial

Build the GDAS App:

.. code-block:: bash

    cd cadre26_noaa_tutorial
    ./build_gdas_cluster.sh

Check executables:

.. code-block:: bash

    cd ../GDASApp
    tail -n 10 build.log
    cd build/bin
    ls


Download JEDI input dataset:

.. code-block:: bash

    wget https://s3.us-east-1.amazonaws.com/epic.sandbox.content/cadre26-input-data.tar.gz
    tar -xvzf cadre26-input-data.tar.gz

Remember the path:

``cadre26/input_data``


Copy YAML files:

.. code-block:: bash

    cd input_yaml
    cp Day1/jedi_3dvar* .
    # or
    cp Day2/<exp_case>/jedi_3dvar* .
    # or
    cp Day3/<exp_case>/jedi_3dvar* .


Edit job submission script:

.. code-block:: bash

    vim run_3dvar_cluster.sh


Submit job:

.. code-block:: bash

    sbatch run_3dvar_cluster.sh

Check job:

.. code-block:: bash

    squeue -u ubuntu

Move to experiment directory:

.. code-block:: bash

    cd exp_case/<EXP_NAME_BASE>.<job_ID>

Check logs:

.. code-block:: bash

    vim OUTPUT.fv3jedi
    vim errfile_fv3jedi


Run Diagnostics
===============

Clone diagnostics:

.. code-block:: bash

    git clone https://github.com/jkbk2004/ufs_da_diagnostics

Set up environment:

.. code-block:: bash

    pip install -e .
    pip install seaborn scipy

Update YAMLs:

.. code-block:: bash

    cd diagnostic/yamls/<exp_case>
    vim increment_maps.yaml
    vim obs_diag.yaml
    vim spectra_bkg_inc.yaml
    vim spectra_ana_inc.yaml

Create test directory:

.. code-block:: bash

    mkdir -p test
    cd test


Day 1 Diagnostics
-----------------

.. code-block:: bash

    ufsda-inc-maps --yaml ../diagnostic/yamls/day1/increment_maps.yaml
    ufsda-obs-diag --yaml ../diagnostic/yamls/day1/obs_diag.yaml
    ufsda-spectra-bkg-inc --yaml ../diagnostic/yamls/day1/spectra_bkg_inc.yaml
    ufsda-jedi-log ../exp_case/<EXP_NAME_BASE>.<job_ID>/OUTPUT.fv3jedi --output day1_log_report.txt


Day 2 (NICAS)
-------------

.. code-block:: bash

    ufsda-inc-maps --yaml ../diagnostic/yamls/day2_nicas_length_scale/increment_maps.yaml
    ufsda-obs-diag --yaml ../diagnostic/yamls/day2_nicas_length_scale/obs_diag.yaml
    ufsda-spectra-ana-inc --yaml ../diagnostic/yamls/day2_nicas_length_scale/spectra_ana_inc.yaml
    ufsda-jedi-log ../exp_case/<EXP_NAME_BASE>.<job_ID>/OUTPUT.fv3jedi --output day2_log_report.txt


Day 3 (ATMS Error)
------------------

.. code-block:: bash

    ufsda-inc-maps --yaml ../diagnostic/yamls/day3_atms_err/increment_maps.yaml
    ufsda-obs-diag --yaml ../diagnostic/yamls/day3_atms_err/obs_diag.yaml
    ufsda-spectra-ana-inc --yaml ../diagnostic/yamls/day3_atms_err/spectra_ana_inc.yaml
    ufsda-jedi-log ../exp_case/<EXP_NAME_BASE>.<job_ID>/OUTPUT.fv3jedi --output day3_log_report.txt


Download Files to Your Laptop
=============================

Add private keys:

.. code-block:: bash

    ssh-add ~/.ssh/epic_workshop.pem
    ssh-add ~/.ssh/<your_other_key>

Create compressed file:

.. code-block:: bash

    cd ..
    tar -cvzf test.tar.gz test

Download via SCP:

.. code-block:: bash

    scp -J <user>@jump.epic.noaa.gov ubuntu@<user>:<path>/test.tar.gz .
    tar -xvzf test.tar.gz

Example:

.. code-block:: bash

    scp -J chanhoo@jump.epic.noaa.gov ubuntu@chanhoo:/home/ubuntu/cadre26_noaa_tutorial/test.tar.gz .

