import numpy as np
import pandas as pd
from netCDF4 import Dataset

# === Input/output ===
nc_file = r"D:\NASA_hackathon_2025\ssh_1\SWOT_L2_LR_SSH_Expert_001_007_20140412T170840_20140412T180007_DG10_01.nc"
output_csv = "ssh.csv"

# Open the NetCDF file
nc = Dataset(nc_file, "r")

# Read variables
lat = nc.variables["lat"][:]
lon = nc.variables["lon"][:]
carbon = nc.variables["carbon_phyto"][:]

# Flatten into table
lat_grid, lon_grid = np.meshgrid(lat, lon, indexing="ij")

df = pd.DataFrame({
    "lat": lat_grid.ravel(),
    "lon": lon_grid.ravel(),
    "carbon_phyto": carbon.ravel()
})

# Save to CSV
df.to_csv(output_csv, index=False)
print(f"✅ Saved {output_csv} with {len(df)} rows.")

nc.close()
