.. _appendix_slurm_basics:

Appendix B — Slurm Basics
=========================

This appendix summarizes the essential Slurm commands required for CADRE
Year‑2 training. These commands apply to Hercules and most HPC systems.

.. contents::
   :local:
   :depth: 2


B.1 Submitting Batch Jobs
-------------------------

Submit a job script::

    sbatch job.slurm

A minimal example job script:

.. code-block:: bash

    #!/bin/bash
    #SBATCH --job-name=test
    #SBATCH --qos=normal
    #SBATCH --time=01:00:00
    #SBATCH --ntasks=1

    srun hostname


B.2 Interactive Jobs
--------------------

Request an interactive compute session::

    salloc --qos=<qos> --time=01:00:00 --ntasks=1

Then run commands inside the allocated node.

Cancel an interactive session::

    exit


B.3 Monitoring Jobs
-------------------

List your jobs::

    squeue -u $USER

List all jobs::

    squeue

Show job details::

    scontrol show job <jobid>


B.4 Job Output and Errors
-------------------------

Slurm writes output to files such as::

    slurm-<jobid>.out

Check job errors inside this file if a job fails.


B.5 Useful Slurm Commands
-------------------------

- Check partitions/QOS::

      sinfo

- Check job efficiency::

      seff <jobid>

- Cancel a job::

      scancel <jobid>


B.6 Summary
-----------

This appendix provides the minimal Slurm commands needed to submit,
monitor, and debug jobs for CADRE Year‑2 training workflows.
