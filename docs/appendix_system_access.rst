.. _appendix_system_access:

Appendix A — System Access and HPC Login
========================================

This appendix provides reference instructions for accessing the Hercules
HPC system from macOS and Windows, including optional X11 forwarding for
GUI applications. These steps support all CADRE Year‑2 training workflows.

.. contents::
   :local:
   :depth: 2


A.1 Login from macOS
--------------------

1. Open the **Terminal** application.
2. Connect to the Hercules login node using SSH::

      ssh -X <username>@hercules-login.hpc.msstate.edu

   The ``-X`` option enables X11 forwarding.

3. (Optional) Install **XQuartz** for GUI/X11 applications:

   - https://www.xquartz.org/

   After installation, log out and log back in to activate X11.


A.2 Login from Windows (PuTTY)
------------------------------

1. Install and open **PuTTY**.
2. Enter the hostname:

   ``hercules-login.hpc.msstate.edu``

3. (Optional) Enable X11 forwarding:

   *Connection → SSH → X11 → “Enable X11 forwarding”*

.. figure:: /_static/images/ssh/putty_x11_forwarding.png
   :alt: PuTTY X11 forwarding settings
   :width: 420px
   :align: center

   PuTTY settings for enabling X11 forwarding.

4. (Optional) Install **Xming** to provide the X11 display server:

   - https://sourceforge.net/projects/xming/

   Start Xming before launching PuTTY.


A.3 Basic Hercules HPC Environment
----------------------------------

After logging in, verify your account and environment::

    id
    groups
    showqos
    pwd

Key items:

- **Username**  
- **Project allocation / Slurm QOS**  
- **Home directory**  
- **Work directory** (e.g., ``/work/<project>/<username>``)


A.4 Filesystem Overview
-----------------------

Hercules provides several storage locations:

- **Home directory** — persistent, backed up  
- **Work directory** — high‑performance storage for experiments  
- **Scratch** — temporary, purged regularly  

Check available space::

    df -h
    du -sh .


A.5 Slurm Usage Basics
----------------------

Submit a batch job::

    sbatch job.slurm

Request an interactive compute session::

    salloc --qos=<qos> --time=01:00:00 --ntasks=1

Check queue status::

    squeue


A.6 X11 Forwarding Notes
------------------------

Test X11 forwarding::

    xclock

If the clock window appears, X11 is working.

Troubleshooting:

- macOS: ensure XQuartz is installed and running  
- Windows: ensure Xming is running before PuTTY  
- SSH must include ``-X``  
- Check ``echo $DISPLAY`` is set  


A.7 Summary
-----------

This appendix provides reference instructions for accessing Hercules from
macOS and Windows, configuring X11 forwarding, and verifying your HPC
environment. These steps support all CADRE Year‑2 training workflows.
