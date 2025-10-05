import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Load your CSV file
csv_file = "training_dataset_07.csv"  # Replace with your file path
df = pd.read_csv(csv_file, parse_dates=['timestamp'])

# Filter for presence = 1 (markers) and presence = 0 (no markers)
present = df[df['presence'] == 1]
absent = df[df['presence'] == 0]

# Create the plot
plt.figure(figsize=(14, 10))
ax = plt.axes(projection=ccrs.PlateCarree())

# Add map features
ax.add_feature(cfeature.LAND, facecolor='lightgray')
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

# Plot presence = 0 (background points)
if len(absent) > 0:
    ax.scatter(
        absent['longitude'], absent['latitude'],
        c='lightgray', s=20, alpha=0.3, label='No Presence (0)',
        transform=ccrs.PlateCarree()
    )

# Plot presence = 1 (shark locations)
if len(present) > 0:
    ax.scatter(
        present['longitude'], present['latitude'],
        c='red', s=50, alpha=0.8, marker='o', 
        edgecolors='darkred', linewidths=1,
        label='Shark Present (1)',
        transform=ccrs.PlateCarree()
    )

# Set map extent based on data
if len(df) > 0:
    margin = 2  # degrees
    ax.set_extent([
        df['longitude'].min() - margin,
        df['longitude'].max() + margin,
        df['latitude'].min() - margin,
        df['latitude'].max() + margin
    ])

plt.title('Shark Presence Locations', fontsize=16, fontweight='bold')
plt.legend(loc='upper right')
plt.tight_layout()
plt.show()

# Print summary
print(f"Total points: {len(df)}")
print(f"Shark present (1): {len(present)}")
print(f"Shark absent (0): {len(absent)}")