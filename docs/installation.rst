Installation
============

The diagnostics toolkit can be installed either from source or as an
editable development environment. The recommended workflow uses a
conda environment with all scientific dependencies included.

Prerequisites
-------------

The following packages are required:

- Python 3.9+
- numpy
- scipy
- matplotlib
- cartopy
- netCDF4
- h5py
- ioda-reader (optional but recommended)
- pyyaml

Optional (for developers):

- sphinx
- sphinx-autodoc-typehints
- sphinx-rtd-theme
- pytest


Creating a Conda Environment
----------------------------

.. code-block:: bash

    conda create -n ufsda python=3.10
    conda activate ufsda

    conda install numpy scipy matplotlib cartopy netcdf4 h5py pyyaml
    pip install ioda-reader


Installing the Diagnostics Toolkit
----------------------------------

Clone the repository:

.. code-block:: bash

    git clone https://github.com/your-org/ufs_da_diagnostics.git
    cd ufs_da_diagnostics

Install in editable mode:

.. code-block:: bash

    pip install -e .

This installs the following CLI tools:

- ``ufsda-spectra-ana-inc``
- ``ufsda-spectra-bkg-inc``
- ``ufsda-increment-maps``
- ``ufsda-obs-diagnostic``
- ``ufsda-log-diagnostic``


Building Documentation
----------------------

.. code-block:: bash

    cd docs
    make html

or

.. code-block:: bash

    python -m sphinx -b html docs docs/_build/html
    python -m sphinx -b latex docs/ docs/_build/latex
    cd docs/_build/latex
    latexmk -xelatex
    
The generated documentation will appear in ``docs/_build/html``.
