import yaml
import xarray as xr
import numpy as np
import netCDF4 as nc
import sys


def get_yaml_from_args():
    """
    Parse command-line arguments and return the YAML config file path.
    Usage:
        python extract_single_obs.py --yaml config.yaml
    """
    yaml_file = "config.yaml"
    if "--yaml" in sys.argv:
        idx = sys.argv.index("--yaml")
        if idx + 1 < len(sys.argv):
            yaml_file = sys.argv[idx + 1]
    return yaml_file


def load_config(yaml_file):
    """
    Load YAML configuration containing:
      - injected_file
      - assimilated_file
      - output_file
    """
    with open(yaml_file, "r") as f:
        return yaml.safe_load(f)


def read_assimilated(diag_file):
    """
    Read assimilated (diag) file and extract:
      - QC2 flags (EffectiveQC2 group)
      - latitude, longitude (MetaData group)

    Returns:
      idx_assim: indices where QC2 == 0 (assimilated obs)
      lat_assim: latitudes of assimilated obs
      lon_assim: longitudes of assimilated obs
    """
    qc2 = xr.open_dataset(diag_file, group="EffectiveQC2")["brightnessTemperature"].values
    meta = xr.open_dataset(diag_file, group="MetaData")
    lat = meta["latitude"].values
    lon = meta["longitude"].values

    # QC2 == 0 means assimilated
    mask = np.all(qc2 == 0, axis=1)

    return np.where(mask)[0], lat[mask], lon[mask]


def read_injected_latlon(inj_file):
    """
    Read latitude and longitude from the injected obs file.
    Only MetaData group is needed here.
    """
    meta = xr.open_dataset(inj_file, group="MetaData")
    lat = meta["latitude"].values
    lon = meta["longitude"].values
    return lat, lon


def pick_tropical(lat_assim, idx_assim, lat_min=-30, lat_max=30):
    """
    Select an assimilated observation inside a tropical latitude band.

    Args:
      lat_assim: latitudes of assimilated obs
      idx_assim: indices of assimilated obs in the diag file
      lat_min, lat_max: tropical band limits

    Returns:
      (chosen_global_index, local_index_within_assimilated_subset)
    """
    mask = (lat_assim >= lat_min) & (lat_assim <= lat_max)
    tropical_indices = np.where(mask)[0]

    if len(tropical_indices) == 0:
        raise RuntimeError("No assimilated obs found in tropical latitude band")

    # Pick the middle tropical obs for reproducibility
    mid = len(tropical_indices) // 2
    return idx_assim[tropical_indices[mid]], tropical_indices[mid]


def find_matching_location(lat_d, lon_d, inj_lat, inj_lon, tol=1e-6):
    """
    Find the matching observation in the injected file by exact lat/lon match.

    Args:
      lat_d, lon_d: selected diag lat/lon
      inj_lat, inj_lon: arrays from injected file
      tol: tolerance for floating-point comparison

    Returns:
      index of matching observation in injected file
    """
    dlat = np.abs(inj_lat - lat_d)
    dlon = np.abs(inj_lon - lon_d)
    mask = (dlat < tol) & (dlon < tol)

    idx = np.where(mask)[0]
    if len(idx) == 0:
        raise RuntimeError("No matching lat/lon found in injected file")

    return idx[0]


def write_single_obs_exact_clone(inj_file, loc_idx, output_file):
    """
    Clone the injected obs file EXACTLY using netCDF4, but slice Location=1.

    This preserves:
      - all groups
      - all variables
      - all attributes
      - all fill values
      - all dimension names and order

    Only the Location dimension is reduced to 1.
    """
    src = nc.Dataset(inj_file, "r")
    dst = nc.Dataset(output_file, "w")

    # Copy global attributes
    for attr in src.ncattrs():
        dst.setncattr(attr, src.getncattr(attr))

    # Copy dimensions (Location → 1)
    for dim_name, dim in src.dimensions.items():
        if dim_name == "Location":
            dst.createDimension("Location", 1)
        else:
            dst.createDimension(dim_name, len(dim))

    def copy_group(src_grp, dst_grp):
        """
        Recursively copy groups, variables, and attributes.
        """
        # Copy group attributes
        for attr in src_grp.ncattrs():
            dst_grp.setncattr(attr, src_grp.getncattr(attr))

        # Copy variables
        for var_name, var_in in src_grp.variables.items():
            fill = getattr(var_in, "_FillValue", None)

            # Create variable with same dtype, dims, fill value
            var_out = dst_grp.createVariable(
                var_name,
                var_in.dtype,
                var_in.dimensions,
                fill_value=fill
            )

            # Copy attributes except _FillValue (already handled)
            for attr in var_in.ncattrs():
                if attr == "_FillValue":
                    continue
                var_out.setncattr(attr, var_in.getncattr(attr))

            # Slice Location dimension
            data = var_in[:]
            if "Location" in var_in.dimensions:
                loc_axis = var_in.dimensions.index("Location")
                slicer = [slice(None)] * len(var_in.dimensions)
                slicer[loc_axis] = slice(loc_idx, loc_idx + 1)
                data = data[tuple(slicer)]

            var_out[:] = data

        # Recursively copy subgroups
        for subgrp_name in src_grp.groups:
            new_subgrp = dst_grp.createGroup(subgrp_name)
            copy_group(src_grp.groups[subgrp_name], new_subgrp)

    # Start recursive copy from root
    copy_group(src, dst)

    src.close()
    dst.close()

    print(f"✔ Exact clone written: {output_file}")


def extract_single_obs(yaml_file):
    """
    Main driver:
      1. Load config
      2. Read assimilated obs (QC2 == 0)
      3. Select a tropical obs
      4. Match it to injected file
      5. Clone injected file with Location=1
    """
    cfg = load_config(yaml_file)

    for sensor, paths in cfg.items():
        inj_file = paths["injected_file"]
        diag_file = paths["assimilated_file"]
        out_file = paths["output_file"]

        print(f"\n=== Processing {sensor} ===")

        # Step 1: read assimilated obs
        idx_assim, lat_assim, lon_assim = read_assimilated(diag_file)

        # Step 2: pick tropical obs
        chosen_idx, mid_idx = pick_tropical(lat_assim, idx_assim)
        lat_d = lat_assim[mid_idx]
        lon_d = lon_assim[mid_idx]

        print(f"Diag tropical lat/lon: ({lat_d:.6f}, {lon_d:.6f})")

        # Step 3: read injected lat/lon
        inj_lat, inj_lon = read_injected_latlon(inj_file)

        # Step 4: find matching obs in injected file
        loc_idx = find_matching_location(lat_d, lon_d, inj_lat, inj_lon)

        print(f"Matched injected index: {loc_idx}")
        print(f"Injected lat/lon: ({inj_lat[loc_idx]:.6f}, {inj_lon[loc_idx]:.6f})")

        # Step 5: write exact clone with Location=1
        write_single_obs_exact_clone(inj_file, loc_idx, out_file)


def main():
    """
    CLI entry point for single-observation extraction.
    Allows running:
        ufsda-single-obs --yaml config.yaml
    """
    yaml_file = get_yaml_from_args()
    extract_single_obs(yaml_file)


if __name__ == "__main__":
    main()
