Observation Diagnostics Overview
================================

The observation diagnostics subsystem processes IODA files and generates
a comprehensive suite of observation‑space diagnostics, including
statistics, histograms, QC summaries, and ATMS‑specific channel and
scan‑position diagnostics. These tools quantify how well the background
and analysis fields fit the observations and complement the increment
and spectral diagnostics. For the mathematical formulation and example
figures, see :ref:`Diagnostics Overview <diagnostics_overview>`.


Subsystem Components
--------------------

The observation diagnostics subsystem consists of the following
components:

- **ObsDiagnostic** — core engine for computing O–B and O–A departures,
  bias, RMS, normalized RMS, and QC‑filtered statistics
- **IODA loaders** — readers for satellite and conventional observation
  files
- **Scalar histograms** — e.g., temperature, humidity, pressure
- **Vector histograms** — e.g., wind components (u, v)
- **ATMS diagnostics** — channel‑wise extended RMS statistics and
  scan‑position bias checks
- **QC summaries** — counts and statistics for QC‑passed and QC‑failed
  observations
- **Plotting utilities** — generation of extended RMS, histogram, and
  scan‑position figures


Innovation‑Space Error Diagnostics
----------------------------------

In addition to standard O–B/O–A statistics, the diagnostics subsystem
includes an innovation‑space error diagnostic based on the Desroziers
method. This tool computes innovation variance, estimated
observation‑error variance, and recommended R‑scaling factors using only
OMB and OMA. It is implemented in
``ufs_da_diagnostics/obs/innovation_br_check.py`` and is intended for
routine monitoring of observation‑error consistency and tuning.

The diagnostic reports:

- **Sd = E[OMB²]** — innovation variance  
- **R_est = E[OMA × OMB]** — Desroziers estimate of true observation‑error variance  
- **Sd/R** — innovation chi‑square proxy  
- **R_est/R** — variance‑scaling factor  
- **HBHᵀ = Sd − R_est** — background‑error contribution  
- **scale_R = R_est / R** — recommended R multiplier  
- **infl_chi** — standard‑deviation inflation needed to reach a target chi‑square

These quantities provide a lightweight, observation‑space method for
evaluating the consistency of assumed observation‑error variances.


Workflow
--------

A typical observation‑diagnostic workflow consists of:

1. **Load IODA file**  
   Read observation values, metadata, and QC flags.

2. **Load H(x) files**  
   Load background and analysis model equivalents for computing O–B and
   O–A departures.

3. **Compute statistics**  
   Compute bias, RMS, normalized RMS, bias‑corrected RMS, and QC‑filtered
   statistics for each variable and channel.

4. **Generate plots**  
   Produce histograms, extended RMS figures, scan‑position diagnostics,
   and QC summaries.

5. **Save outputs**  
   Write statistics tables and figures to the output directory.


Related Tools
-------------

The CLI driver for observation diagnostics is described in
:ref:`Using Observation Diagnostics <usage_observation_tools>`.
