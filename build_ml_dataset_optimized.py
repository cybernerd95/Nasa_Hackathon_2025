import pandas as pd
import xarray as xr
import numpy as np
import glob
import os
from datetime import datetime
from tqdm import tqdm
from scipy.spatial import cKDTree  # Efficient library for nearest-neighbor lookups

# --- 1. CONFIGURATION: UPDATE THESE PATHS ---
BASE_DIR = r"D:\NASA_hackathon_2025"
SHARK_DATA_DIR = os.path.join(BASE_DIR, 'shark_data')

# Paths to your raw daily environmental data folders
CHLOR_DIR = os.path.join(BASE_DIR, 'chlorophyll')
CARBON_DIR = os.path.join(BASE_DIR, 'pythoplankton')
SST_DIR = os.path.join(BASE_DIR, 'SST')
SSH_DIR = os.path.join(BASE_DIR, 'SSH')  # Path to the folder with raw SWOT.nc files


# --- 2. SCRIPT ---

def build_training_dataset_optimized():
    """
    Main function to load shark data, generate background points,
    and efficiently match all environmental data (including raw SWOT files)
    to create a final training dataset.
    """

    # --- STEP A: LOAD AND CLEAN SHARK DATA ---
    print("--- Step A: Loading and cleaning shark data ---")

    try:
        shark_files = glob.glob(os.path.join(SHARK_DATA_DIR, '*.csv'))
        df_list = [pd.read_csv(f) for f in shark_files]
        shark_df = pd.concat(df_list, ignore_index=True)
        print(f"Loaded {len(shark_df)} total rows from {len(shark_files)} file(s).")
    except Exception as e:
        print(f"Error loading shark data: {e}")
        return

    shark_df.rename(columns={'date': 'timestamp', 'lat': 'latitude', 'lon': 'longitude'},
                    inplace=True, errors='raise')
    shark_df['timestamp'] = pd.to_datetime(shark_df['timestamp'])

    start_date = '2014-04-12'
    end_date = '2015-12-31'
    shark_df = shark_df[(shark_df['timestamp'] >= start_date) & (shark_df['timestamp'] <= end_date)]

    if shark_df.empty:
        print(f"Warning: No shark tracking data found between {start_date} and {end_date}.")
        return

    print(f"Filtered to {len(shark_df)} shark presence points for the test month.")

    shark_df['presence'] = 1
    presence_points = shark_df[['timestamp', 'latitude', 'longitude', 'presence']].copy()

    # --- STEP B: GENERATE PSEUDO-ABSENCE (BACKGROUND) POINTS ---
    print("\n--- Step B: Generating pseudo-absence (background) points ---")

    num_absence_points = len(presence_points) * 2
    min_lat, max_lat = presence_points['latitude'].min(), presence_points['latitude'].max()
    min_lon, max_lon = presence_points['longitude'].min(), presence_points['longitude'].max()

    rand_lat = np.random.uniform(min_lat, max_lat, num_absence_points)
    rand_lon = np.random.uniform(min_lon, max_lon, num_absence_points)

    time_range = pd.to_datetime(presence_points['timestamp']).astype(np.int64)
    rand_ts_int = np.random.randint(time_range.min(), time_range.max(), num_absence_points, dtype=np.int64)
    rand_ts = pd.to_datetime(rand_ts_int)

    absence_points = pd.DataFrame({
        'timestamp': rand_ts,
        'latitude': rand_lat,
        'longitude': rand_lon,
        'presence': 0
    })
    print(f"Generated {len(absence_points)} background points.")

    training_df = pd.concat([presence_points, absence_points], ignore_index=True)
    training_df['date'] = training_df['timestamp'].dt.date

    # --- STEP C: EFFICIENTLY MATCH ALL ENVIRONMENTAL DATA ---
    print("\n--- Step C: Matching environmental data by grouping dates ---")

    all_results = []

    for date, group in tqdm(training_df.groupby('date'), desc="Processing days"):

        # --- Part 1: Match MODIS Data ---
        daily_modis_data = {}
        modis_map = {
            'chlor_a': os.path.join(CHLOR_DIR, f"AQUA_MODIS.{date.strftime('%Y%m%d')}.L3m.DAY.CHL.chlor_a.4km.nc"),
            'carbon_phyto': os.path.join(CARBON_DIR, f"AQUA_MODIS.{date.strftime('%Y%m%d')}.L4m.DAY.CARBON.carbon_phyto.4km.nc"),
            'sst': os.path.join(SST_DIR, f"AQUA_MODIS.{date.strftime('%Y%m%d')}.L3m.DAY.SST.sst.4km.nc")
        }

        for var, file_path in modis_map.items():
            if os.path.exists(file_path):
                daily_modis_data[var] = xr.open_dataset(file_path)

        def extract_modis_values(row):
            features = {}
            for var, ds in daily_modis_data.items():
                try:
                    features[var] = ds[var].sel(lat=row['latitude'], lon=row['longitude'], method='nearest').item()
                except Exception:
                    features[var] = np.nan
            return pd.Series(features)

        day_results = group.apply(extract_modis_values, axis=1)

        for ds in daily_modis_data.values():
            ds.close()

        # --- Part 2: Match SWOT Data ---
        # Find all SWOT files that contain the date substring in the filename
        date_str = date.strftime('%Y%m%d')
        swot_files_for_day = [f for f in glob.glob(os.path.join(SSH_DIR, '*.nc')) if date_str in os.path.basename(f)]

        if swot_files_for_day:
            daily_swot_dfs = []
            for swot_file in swot_files_for_day:
                with xr.open_dataset(swot_file) as ds:
                    # Flexible variable detection
                    ssh_var_candidates = ['ssha_karin', 'ssh_karin', 'ssha', 'ssha_karin_2']
                    ssh_var = None
                    for var in ssh_var_candidates:
                        if var in ds.variables:
                            ssh_var = var
                            break
                    if ssh_var is None:
                        continue  # skip if no SSH variable found

                    # Flatten lat/lon and variable
                    df = pd.DataFrame({
                        'latitude': ds['latitude'].values.ravel(),
                        'longitude': ds['longitude'].values.ravel(),
                        'ssha_karin': ds[ssh_var].values.ravel()
                    }).dropna()
                    if not df.empty:
                        daily_swot_dfs.append(df)

            if daily_swot_dfs:
                combined_swot_day = pd.concat(daily_swot_dfs, ignore_index=True)
                swot_coords = combined_swot_day[['latitude', 'longitude']].values
                tree = cKDTree(swot_coords)

                group_coords = group[['latitude', 'longitude']].values
                distances, indices = tree.query(group_coords, k=1)

                day_results['ssha_karin'] = combined_swot_day['ssha_karin'].iloc[indices].values
            else:
                day_results['ssha_karin'] = np.nan
        else:
            day_results['ssha_karin'] = np.nan
        all_results.append(day_results)

    environmental_data = pd.concat(all_results)
    final_df = training_df.join(environmental_data)

    print("\n--- Data Matching Complete ---")
    print("Sample of the final training dataset (now including ssha_karin):")
    print(final_df.head())

    output_file = 'training_dataset_one_month.csv'
    final_df.to_csv(output_file, index=False)
    print(f"\nSuccessfully created '{output_file}'. You are now ready for model training!")


if __name__ == "__main__":
    # You may need to install scipy: pip install scipy
    build_training_dataset_optimized()