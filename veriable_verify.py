import xarray as xr

# Path to your NetCDF file
nc_file = r"D:\NASA_hackathon_2025\chrophyll_dataset\AQUA_MODIS.20141220.L3m.DAY.CHL.chlor_a.4km.nc"

# Open the dataset
ds = xr.open_dataset(nc_file)

# Print dataset info
print("=== Dataset Info ===")
print(ds)

# Print first 5 rows/slices for each variable
print("\n=== First 5 rows of each variable ===")
for var in ds.data_vars:
    data = ds[var]
    
    # If 1D, show first 5 values
    if len(data.shape) == 1:
        print(f"\nVariable: {var}")
        print(data.values[:5])
    
    # If 2D or more, show first 5 rows of first column
    elif len(data.shape) >= 2:
        print(f"\nVariable: {var}")
        print(data.values[:5, :5])  # first 5x5 slice
