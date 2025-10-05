import os
from datetime import datetime, timedelta

# Path to your folder
folder_path = r"D:\NASA_hackathon_2025\chrophyll_dataset"

# Output file for missing dates
output_file_path = r"missing_dates.txt"

# Extract all dates from filenames
dates_in_folder = set()
for f in os.listdir(folder_path):
    if os.path.isfile(os.path.join(folder_path, f)):
        parts = f.split('.')
        if len(parts) > 1:
            date_str = parts[1]  # e.g., '20140101'
            try:
                date_obj = datetime.strptime(date_str, "%Y%m%d")
                dates_in_folder.add(date_obj)
            except ValueError:
                pass  # ignore files with unexpected names

# Find the range of dates
if not dates_in_folder:
    print("No valid dates found in folder!")
else:
    min_date = min(dates_in_folder)
    max_date = max(dates_in_folder)
    
    # Generate all dates in the range and find missing ones
    current_date = min_date
    missing_dates = []
    while current_date <= max_date:
        if current_date not in dates_in_folder:
            missing_dates.append(current_date.strftime("%d/%m/%Y"))
        current_date += timedelta(days=1)
    
    # Write missing dates to the output file
    with open(output_file_path, 'w') as f:
        for d in missing_dates:
            f.write(d + '\n')
    
    print(f"Missing dates written to {output_file_path}")
