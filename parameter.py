import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# --- Step 1: Load the CORRECT dataset ---
try:
    # MODIFICATION: Change the wildcard to select only the 'Expert' files.
    # This tells xarray to ignore the WindWave files and open the ones with SSH data.
    file_path = r"C:\Users\malla\Downloads\SWOT_L2_LR_SSH_Expert_032_166_20250503T222059_20250503T231127_PIC2_01.nc"
    
    ds = xr.open_mfdataset(file_path, 
                           combine='nested', 
                           concat_dim="num_lines", 
                           decode_times=False)
    
    print("Expert dataset loaded successfully!")
    # Let's confirm the right variables are here
    print("\nAvailable data variables:")
    print(list(ds.data_vars))

except FileNotFoundError:
    print(f"Could not find files matching the pattern: {file_path}")
    print("Please check your download folder for files containing 'Expert' or 'Basic' in their name.")
    ds = xr.Dataset()

# --- Step 2: Plot the data ---

# The variable name for SSHA in the Expert/Basic files is often just 'ssha'
# or it could be 'ssha_karin'. We'll check for both.
ssha_var_name = None
if 'ssha' in ds.data_vars:
    ssha_var_name = 'ssha'
elif 'ssha_karin' in ds.data_vars:
    ssha_var_name = 'ssha_karin'

if ssha_var_name:
    print(f"\nFound SSHA variable: '{ssha_var_name}'. Proceeding to plot...")
    
    # Select the specific variable we want to plot
    ssha_to_plot = ds[ssha_var_name]

    # Select the corresponding coordinates
    lon = ds['longitude']
    lat = ds['latitude']

    # Create a figure and a map projection
    fig, ax = plt.subplots(
        figsize=(10, 10),
        subplot_kw={'projection': ccrs.PlateCarree()}
    )

    # Create the 2D plot
    im = ax.pcolormesh(lon, lat, ssha_to_plot, 
                       transform=ccrs.PlateCarree(), 
                       cmap='coolwarm',
                       vmin=-0.5, vmax=0.5)

    # Add map features
    ax.coastlines()
    ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

    # Add a colorbar and a title
    cbar = plt.colorbar(im, ax=ax, orientation='vertical', shrink=0.7)
    cbar.set_label('Sea Surface Height Anomaly (meters)')
    ax.set_title('SWOT SSHA - Revealing Ocean Eddies')

    plt.show()
else:
    print("\nCould not find 'ssha' or 'ssha_karin' in the dataset.")
    print("Please check the list of available variables printed above and update the script if needed.")