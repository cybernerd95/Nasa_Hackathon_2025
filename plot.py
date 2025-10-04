import pandas as pd
import glob
import plotly.express as px

# -----------------------------
# Step 1: Load the first CSV file
# -----------------------------
files = glob.glob(r"E:\Movements of blue sharks in the North Atlantic Ocean using satellite telemetry, 2014-2017\data\*.csv")
if not files:
    raise ValueError("No CSV files found in the folder!")

data = pd.read_csv(files[0])

# -----------------------------
# Step 2: Prepare the data
# -----------------------------
data['date'] = pd.to_datetime(data['date'])
data = data.sort_values('date')

plane_id = data['id'].iloc[0]  # use the first plane ID
print(f"Visualizing plane ID: {plane_id}")

# -----------------------------
# Step 3: Plot full path with markers
# -----------------------------
fig = px.line_geo(
    data,
    lat='lat',
    lon='lon',
    markers=True,
    line_group='id',  # Connect points
    hover_name='id',
    hover_data={'date': True, 'lat': True, 'lon': True},
    projection='natural earth',
    title=f'Movement of {plane_id}'
)

# -----------------------------
# Step 4: Map layout
# -----------------------------
fig.update_geos(
    showcoastlines=True,
    showland=True,
    showcountries=True,
    fitbounds="locations"
)
fig.update_layout(height=600, margin={"r":0,"t":50,"l":0,"b":0})

fig.show()
