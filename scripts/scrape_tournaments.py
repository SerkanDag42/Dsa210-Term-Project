import pandas as pd
from bs4 import BeautifulSoup
import warnings
import re
warnings.filterwarnings('ignore')

print(" Initializing local HTML scraper for Liquipedia...")

# 1. LOAD LOCAL HTML FILE
try:
    with open("data/raw/liquipedia.html", "r", encoding="utf-8") as f:
        html_content = f.read()
except FileNotFoundError:
    print(" ERROR: 'liquipedia.html' not found in the current directory.")
    print("   Please save the webpage manually as 'liquipedia.html' via Ctrl+S.")
    exit()

soup = BeautifulSoup(html_content, 'html.parser')
tournaments_data = []

print(" Extracting and parsing tournament data...")

# 2. DATE PARSER FUNCTION
def parse_liquipedia_date(date_str):
    """
    Converts Liquipedia date strings like 'Nov 30 – Dec 15, 2024' or 'May 14–19, 2024'
    into structured 'YYYY-MM-DD' start and end dates.
    """
    try:
        date_str = date_str.replace('–', '-').replace('\u2013', '-').strip()
        
        if ',' not in date_str:
            return None, None
            
        month_days, year = date_str.split(',')
        year = year.strip()
        
        if '-' in month_days:
            start_str, end_str = month_days.split('-')
            start_str = start_str.strip()
            end_str = end_str.strip()
            
            if end_str.isdigit():
                month = start_str.split(' ')[0]
                end_str = f"{month} {end_str}"
        else:
            start_str = month_days.strip()
            end_str = start_str
            
        start_date = pd.to_datetime(f"{start_str} {year}").strftime('%Y-%m-%d')
        end_date = pd.to_datetime(f"{end_str} {year}").strftime('%Y-%m-%d')
        return start_date, end_date
    except Exception as e:
        return None, None

# 3. HTML PARSING LOGIC
rows = soup.find_all('tr', class_=lambda c: c and 'table2__row--body' in c)

for row in rows:
    tds = row.find_all('td')
    
    if len(tds) >= 4:
        name_td = row.find('td', class_='column__tournament')
        
        if name_td:
            tournament_name = name_td.get_text(strip=True)
            raw_date = tds[3].get_text(strip=True)
            
            if tournament_name and "TBA" not in raw_date and "TBD" not in tournament_name:
                
                start_date, end_date = parse_liquipedia_date(raw_date)
                
                if start_date and end_date:
                    t_type = "Major" if "Major" in tournament_name else "S-Tier"
                    
                    tournaments_data.append({
                        'start_date': start_date,
                        'end_date': end_date,
                        'tournament_name': tournament_name,
                        'tournament_type': t_type
                    })

# 4. EXPORT TO CSV
df = pd.DataFrame(tournaments_data)

if not df.empty:
    df.to_csv('data/raw/tournaments.csv', index=False)
    print(f"SUCCESS: Extracted and formatted {len(df)} tournaments.")
    print("\n--- EXTRACTED DATA SAMPLE ---")
    print(df.head(10))
else:
    print("ERROR: Could not extract data. Please verify the HTML structure.")