import os
import glob
import xarray as xr

# --- CONFIG ---
FOLDER = r"D:\NASA_hackathon_2025\chlorophyll"   # change to your folder path
PATTERN = "*.nc"   # file pattern (all NetCDF files)

# --- SCRIPT ---
bad_files = []

# Find all .nc files in the folder
nc_files = glob.glob(os.path.join(FOLDER, PATTERN))

print(f"Found {len(nc_files)} NetCDF files in {FOLDER}")

for f in nc_files:
    try:
        # Try to open and immediately close
        with xr.open_dataset(f) as ds:
            _ = ds.attrs  # force read some metadata
    except Exception as e:
        print(f"❌ Could not open: {f}")
        print(f"   Error: {e}")
        bad_files.append(f)

# --- Results ---
if bad_files:
    print("\n=== Files that could NOT be opened ===")
    for bf in bad_files:
        print(bf)
else:
    print("\n✅ All files opened successfully!")
