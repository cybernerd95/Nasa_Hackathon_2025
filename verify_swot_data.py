import xarray as xr
import numpy as np
import glob
import os
from tqdm import tqdm

# --- 1. CONFIGURATION ---
BASE_DIR = r'D:\NASA_hackathon_2025' 
SSH_DIR = os.path.join(BASE_DIR, 'SSH')

# --- 2. SCRIPT ---
def verify_swot_content():
    """
    Scans all SWOT.nc files in a directory and reports on the validity
    of the 'ssha_karin' variable.
    """
    print(f"--- Scanning for SWOT files in: {SSH_DIR} ---")
    
    swot_files = sorted(glob.glob(os.path.join(SSH_DIR, 'SWOT_L2_LR_SSH_*.nc')))
    
    if not swot_files:
        print("ERROR: No raw SWOT.nc files found in the specified directory.")
        return

    print(f"Found {len(swot_files)} files to check. Starting verification...\n")
    
    total_points_all_files = 0
    total_valid_points_all_files = 0
    valid_files = []   # keep track of files with any valid data
    empty_files = []   # keep track of files that are all NaN

    # Use tqdm for a progress bar
    for file_path in tqdm(swot_files, desc="Checking SWOT files"):
        try:
            with xr.open_dataset(file_path) as ds:
                if 'ssha_karin' in ds.variables:
                    variable = ds['ssha_karin']
                    
                    total_elements = variable.size
                    nan_count = np.isnan(variable).sum().item()
                    valid_count = total_elements - nan_count
                    
                    total_points_all_files += total_elements
                    total_valid_points_all_files += valid_count
                    
                    if valid_count == 0:
                        empty_files.append(os.path.basename(file_path))
                        print(f"  - File: {os.path.basename(file_path)} -> VERDICT: EMPTY (100% NaN values)")
                    else:
                        valid_files.append(os.path.basename(file_path))
                        print(f"  - File: {os.path.basename(file_path)} -> VERDICT: VALID ({valid_count} values)")
                else:
                    print(f"  - File: {os.path.basename(file_path)} -> VERDICT: 'ssha_karin' variable NOT FOUND")

        except Exception as e:
            print(f"  - Could not process file {os.path.basename(file_path)}. Error: {e}")

    print("\n--- Verification Complete ---")
    
    if total_points_all_files > 0:
        valid_percentage = (total_valid_points_all_files / total_points_all_files) * 100
        print(f"Total data points scanned across all files: {total_points_all_files}")
        print(f"Total VALID data points found: {total_valid_points_all_files}")
        print(f"Overall data validity: {valid_percentage:.2f}%")

        print("\n=== Files with VALID ssha_karin values ===")
        if valid_files:
            for f in valid_files:
                print("  ", f)
        else:
            print("  None")

        print("\n=== Files with EMPTY ssha_karin (all NaN) ===")
        if empty_files:
            for f in empty_files:
                print("  ", f)
        else:
            print("  None")
    else:
        print("No data points were found to analyze.")

if __name__ == "__main__":
    verify_swot_content()
