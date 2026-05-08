.. _appendix_filesystem_modules:

Appendix C — Hercules Filesystem and Environment Modules
========================================================

This appendix describes the Hercules filesystem layout and the module
environment used for CADRE Year‑2 training.

.. contents::
   :local:
   :depth: 2


C.1 Filesystem Overview
-----------------------

Hercules provides several storage locations:

- **Home directory**  
  Persistent, backed up, small quota. Suitable for scripts and configs.

- **Work directory**  
  High‑performance storage for experiments and large datasets::

      /work/<project>/<username>

- **Scratch** (if available)  
  Temporary storage, purged regularly.

Check available space::

    df -h
    du -sh .


C.2 Recommended Directory Structure
-----------------------------------

A typical CADRE training layout::

    $HOME/cadre2026/
        ├── scripts/
        ├── logs/
        └── experiments/
              ├── day1/
              ├── day2/
              └── day3/


C.3 Environment Modules
-----------------------

Hercules uses the **Lmod** module system.

List available modules::

    module avail

Load a module::

    module load <module>

Unload a module::

    module unload <module>

Show currently loaded modules::

    module list


C.4 CADRE‑Related Modules
-------------------------

Typical modules used for FV3‑JEDI and diagnostics include:

- compilers (GNU, Intel, or LLVM)
- MPI libraries
- Python environments
- NetCDF / HDF5
- JEDI stack modules (if provided)

Example::

    module load jedi/intel-impi
    module load python/3.10


C.5 Environment Troubleshooting
-------------------------------

- If a module fails to load, try::

      module purge

- If Python cannot find packages, verify::

      which python
      python -m pip list

- If JEDI executables are missing, check your module stack.


C.6 Summary
-----------

This appendix provides a reference for the Hercules filesystem layout and
module environment required for CADRE Year‑2 training workflows.
