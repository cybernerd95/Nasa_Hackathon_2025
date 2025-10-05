import os
import webbrowser
import time

# Path to your TXT file containing the links
txt_file = "matching_links.txt"

# Read links from txt file
with open(txt_file, "r") as f:
    links = [line.strip() for line in f if line.strip()]

batch_size = 3
wait_time = 10  # seconds

print(f"Opening {len(links)} links in your default browser in batches of {batch_size}...")

for i in range(0, len(links), batch_size):
    batch = links[i:i+batch_size]
    print(f"\nOpening batch {i//batch_size + 1} ({len(batch)} links)...")
    
    for url in batch:
        try:
            webbrowser.open(url)  # opens in default browser
            print(f"🌐 Opened: {url}")
        except Exception as e:
            print(f"❌ Failed: {url} | Error: {e}")
    
    print(f"⏳ Waiting {wait_time} seconds before next batch...")
    time.sleep(wait_time)

print("\n🎉 All links processed.")
