import requests
import pandas as pd
import time
import urllib.parse
import re
import json
import os
from datetime import datetime

# File paths
TXT_FILE = "itemler.txt"
CSV_FILE = "dsa210_mega_data.csv"

# Read TXT file
if not os.path.exists(TXT_FILE):
    print(f"ERROR: {TXT_FILE} not found. Please create the list.")
    exit()

with open(TXT_FILE, "r", encoding="utf-8") as f:
    # Trim whitespace and skip empty lines
    items_to_track = [line.strip() for line in f.readlines() if line.strip()]

master_df = pd.DataFrame()

# If existing data exists, load it (Resume logic)
if os.path.exists(CSV_FILE):
    master_df = pd.read_csv(CSV_FILE)
    master_df['date'] = pd.to_datetime(master_df['date'])
    existing_items = master_df.columns.tolist()
    
    # Exclude already downloaded items
    items_to_track = [item for item in items_to_track if item not in existing_items]
    print(f"✅ CSV file found! Already downloaded items will be skipped.")

print(f"🚀 MEGA OPERATION: Found {len(items_to_track)} new items to fetch!")
print("-" * 60)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

for index, item in enumerate(items_to_track):
    print(f"[{index+1}/{len(items_to_track)}] Fetching: {item}")
    
    encoded_item = urllib.parse.quote(item)
    url = f"https://steamcommunity.com/market/listings/730/{encoded_item}"
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            match = re.search(r'var line1=([^;]+);', response.text)
            
            if match:
                data_str = match.group(1)
                data_list = json.loads(data_str)
                
                parsed_data = []
                for row in data_list:
                    raw_date = row[0][:11] 
                    date_obj = datetime.strptime(raw_date, "%b %d %Y").date()
                    
                    # Focus on CS2 era (post-2023)
                    if date_obj >= datetime.strptime("2023-01-01", "%Y-%m-%d").date():
                        parsed_data.append({'date': date_obj, item: row[1]})
                
                if len(parsed_data) > 0:
                    temp_df = pd.DataFrame(parsed_data)
                    temp_df['date'] = pd.to_datetime(temp_df['date'])
                    temp_df[item] = pd.to_numeric(temp_df[item], errors='coerce')
                    temp_df = temp_df.groupby('date').mean().reset_index()
                    
                    if master_df.empty:
                        master_df = temp_df
                    else:
                        master_df = pd.merge(master_df, temp_df, on='date', how='outer')
                    
                    # Save after each item
                    save_df = master_df.sort_values('date').ffill()
                    try:
                        save_df.to_csv(CSV_FILE, index=False)
                        print(f"  -> Success! {item} written to CSV.")
                    except PermissionError:
                        print("  -> WARNING: CSV file is open. Please close it; will retry next iteration.")
                else:
                    print(f"  -> Skipped: No data found after 2023.")
            else:
                print("  -> Error: Item name might be incorrect or no listings available.")
        
        elif response.status_code == 429:
            print("  -> WARNING (429): Steam rate limit exceeded. SCRIPT STOPPED.")
            print(f"  -> {CSV_FILE} is safe. Wait 10-15 minutes before running the script again.")
            print("  -> Already downloaded items will be automatically skipped on resume!")
            break
        else:
            print(f"  -> Error code: {response.status_code}")
            
    except Exception as e:
        print(f"  -> Unexpected error (Skipped): {e}")
    
    # 18-second sleep to respect Steam's rate limit
    if index < len(items_to_track) - 1:
        time.sleep(18)

print("-" * 60)
print(f"🎉 OPERATION HALTED OR FINISHED. Current file: {CSV_FILE}")