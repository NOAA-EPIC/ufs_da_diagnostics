Single-Observation Extraction
=============================

This page describes how to extract a single observation from an IODA
observation file using the ``ufs-da-diagnostics`` extraction utilities.
This workflow is useful for debugging, training, and controlled
experiments such as single-observation impact studies.

Overview
--------

The extraction tool performs the following steps:

1. Reads an assimilated diagnostics file (``EffectiveQC2`` and ``MetaData`` groups)
2. Selects an assimilated observation inside a tropical latitude band
3. Matches the selected observation to the injected (raw) observation file
4. Creates a new IODA ObsGroup file containing **exactly one** observation
5. Preserves all groups, variables, attributes, and fill values

The resulting file is fully compatible with FV3-JEDI for ``hofx`` or
variational single-observation experiments.

Configuration
-------------

The extraction tool is driven by a YAML configuration file:

.. code-block:: yaml

    atms_n20:
      injected_file: /path/to/obs.20240224.t00z.atms_n20.nc
      assimilated_file: /path/to/diag.20240224.t00z.atms_n20.nc
      output_file: single.obs.20240224.t00z.atms_n20.nc

Multiple sensors may be listed in the same configuration file.

Running the Tool
----------------

After installation, the command-line interface is available as:

.. code-block:: bash

    ufsda-single-obs --yaml config.yaml

This produces a new single-observation file for each sensor listed in
the configuration.

Python API
----------

The extraction tool may also be called directly from Python:

.. code-block:: python

    from ufs_da_diagnostics.extraction import extract_single_obs
    extract_single_obs("config.yaml")

Output Structure
----------------

The resulting file is a valid IODA ObsGroup file with:

- ``Location = 1``
- All original groups preserved (``MetaData``, ``ObsValue``, etc.)
- All variable attributes preserved
- All fill values preserved
- Only the selected observation retained

Example Use Cases
-----------------

- Single-observation ``hofx`` experiments
- Single-observation 3DVar or hybrid-3DVar tests
- Observation-space debugging
- Training and demonstration workflows

``ufs-da-diagnostics`` ensures that the extracted file is structurally
identical to the original injected file, except for the reduced
``Location`` dimension.
