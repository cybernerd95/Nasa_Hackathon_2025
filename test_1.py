import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np

# --- Step 1: Load the dataset using the 'netcdf4' engine ---
try:
    file_path = r"D:\NASA_hackathon_2025\chrophyll_dataset\AQUA_MODIS.20140101.L4m.DAY.CARBON.carbon_phyto.4km.nc"
    
    # Use the 'netcdf4' engine, which is correct for this file type
    ds = xr.open_dataset(file_path, engine='netcdf4')
    
    print("MODIS dataset loaded successfully with the 'netcdf4' engine!")
    
    print("\nAvailable data variables:")
    print(list(ds.data_vars))

except FileNotFoundError:
    print(f"Could not find the file: {file_path}")
    ds = xr.Dataset()
except Exception as e:
    print(f"An error occurred: {e}")
    ds = xr.Dataset()

# --- Step 2: Plot the data ---

variable_to_plot = 'carbon_phyto' 

if variable_to_plot in ds:
    print(f"\nFound variable: '{variable_to_plot}'. Proceeding to plot...")
    
    data = ds[variable_to_plot]
    lon = ds['lon']
    lat = ds['lat']

    fig, ax = plt.subplots(
        figsize=(12, 8),
        subplot_kw={'projection': ccrs.PlateCarree()}
    )

    im = ax.pcolormesh(lon, lat, np.log10(data), 
                       transform=ccrs.PlateCarree(), 
                       cmap='viridis')

    ax.coastlines()
    ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

    cbar = plt.colorbar(im, ax=ax, orientation='vertical', shrink=0.7)
    cbar.set_label('Log10 of Phytoplankton Carbon (mg/m^3)')
    ax.set_title('MODIS Phytoplankton Carbon - Base of the Marine Food Web')

    plt.show()
else:
    print(f"\nCould not find '{variable_to_plot}' in the dataset.")
    if 'data_vars' in ds:
        print("Please check the list of available variables printed above and update the script if needed.")