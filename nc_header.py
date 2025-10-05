from netCDF4 import Dataset

# === Enter your NetCDF file name here ===
nc_file = "chlor_a\AQUA_MODIS.20140101.L3m.DAY.CHL.chlor_a.4km.nc"

# Open file
nc = Dataset(nc_file, "r")



print("\n=== Variables ===")
for var_name, var in nc.variables.items():
    print(f"\nVariable: {var_name}")
    

nc.close()
