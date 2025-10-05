import datetime

# Paths to your files
links_file_path = r"D:\NASA_hackathon_2025\link.txt"      # file with URLs
dates_file_path = r"D:\NASA_hackathon_2025\missing_dates.txt"     # file with dates to match
output_file_path = r"matching_links.txt"  # output file

# Read dates and convert them to YYYYMMDD format for comparison
dates_to_match = set()
with open(dates_file_path, 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        # Check if date is in DD/MM/YYYY format
        try:
            date_obj = datetime.datetime.strptime(line, "%d/%m/%Y")
            date_str = date_obj.strftime("%Y%m%d")
        except ValueError:
            # If already in YYYYMMDD format
            date_str = line
        dates_to_match.add(date_str)

# Read links and keep only those that match the dates
matching_links = []
with open(links_file_path, 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        # Extract date from link
        try:
            filename = line.split('/')[-1]  # get last part of URL
            file_date = filename.split('.')[1]  # second part is YYYYMMDD
            if file_date in dates_to_match:
                matching_links.append(line)
        except IndexError:
            continue  # skip malformed lines

# Write matching links to output file
with open(output_file_path, 'w') as f:
    for link in matching_links:
        f.write(link + '\n')

print(f"Matching links written to {output_file_path}")
