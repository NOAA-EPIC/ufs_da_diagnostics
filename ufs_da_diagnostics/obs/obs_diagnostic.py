"""
obs_diagnostic.py

This module is the *orchestrator* for UFS DA observation diagnostics.
It is intentionally lightweight and contains NO plotting logic.

Responsibilities:
  • Load YAML configuration
  • Construct ObsDiagPlotter (the real plotting engine)
  • Dispatch diagnostics for each observation type
  • Provide the `main()` function required by the CLI tool:
        ufsda-obs-diag --yaml config.yaml

All heavy plotting lives in:
    ufs_da_diagnostics/plots/obs_diag_plotter.py
"""

import os
import yaml
from netCDF4 import Dataset

# The real plotting engine lives in plots/
from ..plots.obs_diag_plotter import ObsDiagPlotter


# ============================================================
# ObsDiagPlotter Wrapper
# ============================================================

class ObsDiagPlotterWrapper:
    """
    Wrapper class that:
      • Loads YAML config
      • Instantiates ObsDiagPlotter
      • Runs diagnostics

    This keeps obs_diagnostic.py clean and import‑safe.
    """

    def __init__(self, config_path):
        self.config_path = config_path

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"YAML config not found: {config_path}")

        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        # Create the plotting engine
        self.plotter = ObsDiagPlotter(self.config)

    def run(self):
        """Run all diagnostics defined in the YAML."""
        print(f"[INFO] Loaded YAML: {self.config_path}")
        self.plotter.run()


# ============================================================
# CLI Entry Point (required by ufsda-obs-diag)
# ============================================================

def main():
    """
    Entry point for the CLI tool `ufsda-obs-diag`.

    The CLI wrapper executes:
        from ufs_da_diagnostics.obs.obs_diagnostic import main
        sys.exit(main())

    This function:
      1. Parses --yaml argument
      2. Loads YAML config
      3. Runs ObsDiagPlotterWrapper
    """
    import argparse

    parser = argparse.ArgumentParser(description="UFS DA Observation Diagnostics")
    parser.add_argument("--yaml", required=True, help="YAML configuration file")
    args = parser.parse_args()

    wrapper = ObsDiagPlotterWrapper(args.yaml)
    wrapper.run()

    return 0  # required for sys.exit(main())
