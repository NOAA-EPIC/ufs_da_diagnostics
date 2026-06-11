.. _usage_innovation_br_check:

Using Innovation-Space Error Diagnostics
========================================

The ``innovation_br_check.py`` tool computes innovation‑space error
diagnostics based on the Desroziers et al. (2005) method. These
diagnostics estimate the statistical consistency between the background,
the observations, and the assumed observation‑error variance ``R`` using
only the innovations:

* **OMB** = H(x_b) − y  
* **OMA** = H(x_a) − y

This method provides a lightweight, observation‑space approach for
evaluating whether the specified observation‑error variance is
appropriate and for guiding tuning of ``R`` in UFS DA workflows.


Running the Tool
----------------

Execute the diagnostic with:

::

    python innovation_br_check.py --yaml obs_diag.yaml

The YAML file must contain paths to OMB, OMA, R, QC, and channel or
variable metadata. The structure matches the configuration used by the
standard ``obs_diag`` utilities.


Mathematical Formulation
------------------------

The innovation‑space diagnostic computes the following quantities for
each channel or scalar observation type:

``Sd = E[OMB^2]``
    Innovation variance. Represents ``HBH^T + R_true``.

``R_est = E[OMA * OMB]``
    Desroziers estimate of the true observation‑error variance.

``Sd/R``
    Innovation chi‑square proxy.  
    Values < 1 → assumed ``R`` too large.  
    Values > 1 → assumed ``R`` too small.

``R_est/R``
    Ratio of estimated to assumed observation‑error variance.  
    This is the Desroziers variance‑scaling factor.

``HBH^T = Sd - R_est``
    Background‑error contribution to the innovation variance.

``HBH^T/R``
    Background‑to‑observation ratio.  
    Values below ~0.3 are typical for microwave radiances.

``scale_R = R_est / R``
    Recommended multiplier for tuning the assumed observation‑error
    variance.

``infl_chi = sqrt((Sd/R) / chi_target)``
    Standard‑deviation inflation needed to achieve a target chi‑square
    (default ``chi_target = 0.8``).


Interpretation Guidelines
-------------------------

These diagnostics provide insight into the statistical consistency of the
assumed observation‑error variance:

* **Sd/R < 1**  
  Assumed ``R`` is too large; observations are under‑weighted.

* **Sd/R > 1**  
  Assumed ``R`` is too small; observations are over‑weighted.

* **R_est/R < 1**  
  Estimated observation‑error variance is smaller than assumed.

* **R_est/R > 1**  
  Estimated observation‑error variance is larger than assumed.

* **HBH^T/R small (0.0–0.3)**  
  Background contribution is modest and typical for many radiance
  channels.

* **scale_R**  
  Direct multiplier for tuning the assumed observation‑error variance.

* **infl_chi**  
  Standard‑deviation inflation needed to achieve a target chi‑square.


Example Output
--------------

A typical diagnostic output for a radiance channel::

    Ch 09: Sd/R=0.158  R_est/R=0.114  HBH^T=0.018  HBH^T/R=0.044
           scale_R=0.114  infl_chi=0.445

Interpretation:

* ``Sd/R`` well below 1 → assumed ``R`` is too large.  
* ``R_est/R`` confirms the same.  
* ``HBH^T/R`` small → background contribution is modest.  
* ``scale_R`` suggests reducing the assumed variance.  
* ``infl_chi`` suggests reducing the standard deviation.


Use Cases
---------

The innovation‑space diagnostic is useful for:

* monitoring observation‑error consistency,
* identifying channels with mis‑specified ``R``,
* guiding observation‑error tuning,
* validating new observation types,
* comparing background‑error contributions across cycles.

Because the method uses only OMB and OMA, it is computationally cheap and
can be applied to large datasets or multiple cycles with minimal
overhead.


Integration with UFS DA Diagnostics
-----------------------------------

``innovation_br_check.py`` is part of the observation‑diagnostics
subsystem and complements:

* O–B/O–A statistics,
* extended RMS diagnostics,
* ATMS channel and scan‑position diagnostics,
* QC summaries.

It provides an additional, statistically grounded view of observation‑error
performance that is not available from standard O–B/O–A metrics alone.
