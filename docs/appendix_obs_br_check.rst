.. _appendix-obs-br-check:

Appendix X: Innovation-Space Diagnostics with ``ufsda-obs-br-check``
====================================================================

Overview
--------

The ``ufsda-obs-br-check`` utility computes *innovation-space diagnostics*
for radiance observations using the Desroziers (2005) method. These
diagnostics assess the statistical consistency between:

* the background state,
* the background-error covariance,
* the analysis state (through OMA),
* the observations, and
* the assumed observation-error variance ``R``.

All quantities are derived **entirely from innovations** and do *not*
depend on the full analysis increment or the Kalman gain.


Innovation Definitions
----------------------

The tool uses the standard JEDI sign convention:

``OMB = y - H(x_b)``
    Observation minus background.

``OMA = y - H(x_a)``
    Observation minus analysis.

These definitions ensure consistency with the Desroziers identities:

* ``Sd     = E[OMB^2]``
* ``R_est  = E[OMA * OMB]``
* ``HBH^T  = Sd - R_est``


Background State vs Background Covariance Contribution
------------------------------------------------------

Two distinct concepts appear in innovation diagnostics:

``Background state contribution``
    The *direct mismatch* between the background and the observation,
    represented by the innovation ``OMB = y - H(x_b)``. This measures
    how far the background state is from the observation.

``Background covariance contribution``
    The *portion of the innovation variance* explained by background
    error, given by ``HBH^T = Sd - R_est``. This is a covariance-level
    quantity and reflects how much background-error variance contributes
    to the innovations.

These two contributions are fundamentally different: one is a state
difference, the other is a variance decomposition.


Analysis-State Contribution
---------------------------

Although these diagnostics operate entirely in observation space, the
analysis state does appear through the quantity

``OMA = y - H(x_a)``

which is used in the Desroziers identity

``R_est = E[OMA * OMB]``.

This use of the analysis state does *not* evaluate the analysis increment
or the Kalman gain.  Instead, ``OMA`` serves only as a statistical probe
to estimate the true observation-error variance.  In this sense, the
analysis contributes to the diagnostics, but only through its projection
into observation space, and only for the purpose of variance estimation.


Diagnostic Quantities
---------------------

For each channel, the following innovation-space quantities are computed:

``Sd = E[OMB^2]``
    Innovation variance. Equal to ``HBH^T + R_true``.

``R_est = E[OMA * OMB]``
    Desroziers estimate of the true observation-error variance.

``Sd/R``
    Innovation chi-square proxy. Values much less than 1 indicate that
    the assumed ``R`` is too large; values much greater than 1 indicate
    that ``R`` is too small.

``R_est/R``
    Ratio of estimated to assumed observation-error variance. Used as a
    variance scaling indicator.

``HBH^T = Sd - R_est``
    Background-error contribution to the innovation variance.

``HBH^T/R``
    Background-to-observation ratio. Values below ~0.3 are typical for
    microwave radiances.

``scale_R = R_est / R``
    Recommended variance multiplier for tuning the assumed ``R``.

``infl_chi = sqrt((Sd/R) / chi_target)``
    Standard-deviation inflation factor required to achieve a target
    chi-square (default ``chi_target = 0.8``).


Interpretation Guidelines
-------------------------

* **Sd/R < 1**  
  The assumed ``R`` is too large; observations are under-weighted.

* **Sd/R > 1**  
  The assumed ``R`` is too small; observations are over-weighted.

* **HBH^T/R small (0.0–0.3)**  
  Background covariance contribution is modest and typical for ATMS.

* **scale_R < 1**  
  Decrease the assumed observation-error variance.

* **scale_R > 1**  
  Increase the assumed observation-error variance.

* **infl_chi**  
  Recommended per-channel standard-deviation inflation to achieve the
  target chi-square.


Example Output
--------------

::

    Ch 09: Sd/R=0.158  R_est/R=0.114  HBH^T=0.018  HBH^T/R=0.044
           scale_R=0.114  infl_chi=0.445

Interpretation:

* ``Sd/R`` is well below 1 → assumed ``R`` is too large.
* ``R_est/R`` confirms the same.
* ``HBH^T/R`` is small → background covariance contribution is modest.
* ``infl_chi`` suggests multiplying the standard deviation by ~0.45
  (a reduction of about 55%).


Usage
-----

Run the tool with:

::

    ufsda-obs-br-check --yaml obs_diag.yaml

The utility reads ``OMB``, ``OMA``, ``R``, and ``QC`` from the
``obs_diag.yaml`` file and prints per-channel diagnostics.


Notes
-----

These diagnostics operate entirely in innovation space and should be
interpreted as statistical consistency checks on ``R`` and background
error contributions.
