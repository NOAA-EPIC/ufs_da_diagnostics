Using Log Diagnostics
=====================

The log diagnostics subsystem parses a full JEDI variational DA log and
extracts structured diagnostics including configuration metadata,
observation counts, Jo evolution, cost‑function convergence, departures,
and chi‑squared consistency information. These diagnostics complement
the increment, spectra, and observation‑space tools by providing insight
into the internal behavior of the variational minimization. For a
high‑level description, see :ref:`Diagnostics Overview
<diagnostics_overview>`.


Running the CLI Tool
--------------------

The log diagnostics tool does **not** use a YAML configuration.
It is invoked directly from the command line:

.. code-block:: bash

    ufsda-jedi-log jedi.log

To write the full human‑readable report to a file:

.. code-block:: bash

    ufsda-jedi-log jedi.log --output report.txt

The tool scans the entire JEDI log file and extracts structured
diagnostic fields, producing a formatted text report and optional plots.


Chi‑Squared Consistency Check
-----------------------------

The log parser extracts Jo, Jb, and total cost values at each iteration
and computes the chi‑squared consistency metric:

.. math::

    \chi^2 = \frac{\mathrm{Jo}}{p}

where :math:`p` is the number of assimilated observations. Values near
unity indicate consistency between observation errors, background
errors, and the resulting analysis increments.


Outputs
-------

When ``--output`` is used, the following files are produced:

- ``report.txt`` — formatted human‑readable diagnostic report
- ``jo_evolution.png`` — Jo evolution across outer iterations
- ``cost_convergence.png`` — total cost, Jb, and Jo convergence

These outputs provide a structured view of the variational minimization
and help diagnose issues related to observation errors, background
errors, and convergence behavior.


Example Report (Excerpt)
------------------------

Below is a shortened excerpt of the generated ``report.txt``:

.. code-block:: text

    ================================================================================
      JEDI Variational DA - Diagnostic Report
    ================================================================================

      1. CONFIGURATION SUMMARY
      ------------------------
      Cost Type          : 3D-Var
      Analysis Time      : 2024-02-24T00:00:00Z
      Window Length      : PT6H
      Outer Resolution   : C96
      Inner Resolution   : C48
      Ensemble Members   : 2

      2. OBSERVATION COUNTS
      ----------------------
      Obs Type                Total Obs   Assimilated   Assim%
      conventional_ps          116,459       107,491     92.3%
      gnssro_cosmic2           363,132       227,802     62.7%
      ATMS N20                 245,124       167,540     68.3%

      3. Jo/n EVOLUTION
      ------------------
      ATMS N20   0.186 -> 0.154 -> 0.126

      4. COST FUNCTION CONVERGENCE
      -----------------------------
      Outer 0: J = 149,138 → 136,351
      Outer 1: J = 136,732 → 121,229

      5. CHI-SQUARED CONSISTENCY
      ---------------------------
      ATMS N20   Jo/P = 0.126   (overestimated)
