#!/usr/bin/env python3
"""
Observation Diagnostics Driver
==============================

This module provides a lightweight command‑line interface for running the
observation‑level diagnostics in ``ufs_da_diagnostics``. It loads a YAML
configuration file describing the observations to process and dispatches
all requested diagnostics through the ``ObsDiagPlotter`` orchestrator.

Typical usage:

    $ python obs_diagnostic.py --yaml obs_plots.yaml

The YAML file specifies observation types (ATMS, scalar, vector),
diagnostics to run (histograms, stats, extended stats, scan‑position,
latitude‑binned), and output directories. See the user guide for details.
"""

import os
import sys
import argparse
import yaml

from ..plots.obs_diag_plotter import ObsDiagPlotter


def parse_args():
    """
    Parse command‑line arguments.

    Returns
    -------
    argparse.Namespace
        Parsed arguments containing:

        - ``yaml``: Path to the YAML configuration file.
    """
    p = argparse.ArgumentParser()
    p.add_argument("--yaml", required=True, help="YAML config for obs diagnostics")
    return p.parse_args()


def main():
    """
    Main entry point for running observation diagnostics.

    Steps
    -----
    1. Parse command‑line arguments.
    2. Load the YAML configuration.
    3. Instantiate ``ObsDiagPlotter`` with the configuration.
    4. Execute all requested diagnostics.

    Notes
    -----
    - The YAML file controls all diagnostics behavior.
    - Output directories are created automatically by the plotter.
    """
    args = parse_args()
    with open(args.yaml, "r") as f:
        cfg = yaml.safe_load(f)

    print(f"[INFO] Loaded config: {args.yaml}")
    plotter = ObsDiagPlotter(cfg)
    plotter.run()


if __name__ == "__main__":
    main()

