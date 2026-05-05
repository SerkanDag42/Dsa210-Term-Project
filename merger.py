import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. LOAD DATA
csv_file = "dsa210_mega_data.csv" 
twitch_file = "cs2_gunluk_izleyici.csv"

print("1. Loading datasets...")
try:
    df_market = pd.read_csv(csv_file)
    df_twitch = pd.read_csv(twitch_file)
except FileNotFoundError as e:
    print(f"ERROR: File not found! {e}")
    exit()

df_market['date'] = pd.to_datetime(df_market['date'])
df_twitch['date'] = pd.to_datetime(df_twitch['tarih']).dt.tz_localize(None).dt.normalize()

df = pd.merge(df_market, df_twitch[['date', 'ort_izleyici']], on='date', how='left')

# ==========================================
# 2. PRO TOURNAMENT CALENDAR (DATA ENRICHMENT)
# ==========================================
print("2. Processing Tournament Calendar into the dataset...")

# Tournaments: (Start, End, Name, Plot Color, Text Height Offset)
turnuvalar = [
    # MAJOR TOURNAMENTS (Vibrant Colors)
    ('2023-05-08', '2023-05-21', 'Paris Major 23', 'cyan', 0.95),
    ('2024-03-17', '2024-03-31', 'Copenhagen Major 24', 'orange', 0.95),
    ('2024-11-30', '2024-12-15', 'Shanghai Major 24', 'red', 0.95),
    ('2025-06-03', '2025-06-22', 'Austin Major 25', 'purple', 0.95),
    ('2025-11-24', '2025-12-14', 'Budapest Major 25', 'magenta', 0.95),
    ('2026-11-25', '2026-12-13', 'Singapore Major 26', 'blue', 0.95),
    
    # S-TIER PRO TOURNAMENTS (Gray to avoid visual clutter)
    ('2024-01-31', '2024-02-11', 'Katowice 24', 'gray', 0.85),
    ('2024-07-17', '2024-07-21', 'EWC Riyadh 24', 'gray', 0.85),
    ('2024-08-07', '2024-08-18', 'Cologne 24', 'gray', 0.85),
    ('2025-01-29', '2025-02-09', 'Katowice 25', 'gray', 0.85),
    ('2025-07-23', '2025-08-03', 'Cologne 25', 'gray', 0.85),
    ('2026-01-28', '2026-02-08', 'Krakow 26', 'gray', 0.85)
]

# Function for tournament labeling
def get_tournament_name(date_val):
    for start, end, name, _, _ in turnuvalar:
        if pd.to_datetime(start) <= date_val <= pd.to_datetime(end):
            return name
    return 'Normal Period'

df['Tournament'] = df['date'].apply(get_tournament_name)

enriched_file = "enriched_market_data.csv"
df.to_csv(enriched_file, index=False)
print(f"✅ Table enriched: '{enriched_file}' is ready.")
print("-" * 60)

# ==========================================
# 3. DUAL-AXIS EXPLORATORY DATA ANALYSIS (EDA)
# ==========================================
print("3. Generating Dual-Axis EDA Plot...")

# TOTAL PORTFOLIO VALUE (SUM)
item_columns = [col for col in df.columns if col not in ['date', 'Tournament', 'ort_izleyici', 'tarih']]
df['Market_Index'] = df[item_columns].sum(axis=1)

# Plot Configuration (High width for timeline clarity)
fig, ax1 = plt.subplots(figsize=(22, 8)) 
sns.set_theme(style="whitegrid")

# PRIMARY AXIS: MARKET PORTFOLIO
color1 = '#1f77b4'
ax1.set_xlabel('Date', fontsize=14, fontweight='bold')
ax1.set_ylabel('Total Portfolio Value ($)', color=color1, fontsize=14, fontweight='bold')
sns.lineplot(data=df, x='date', y='Market_Index', ax=ax1, color=color1, linewidth=2.5, label='CS2 Portfolio Index')
ax1.tick_params(axis='y', labelcolor=color1)

# SECONDARY AXIS: TWITCH VIEWERSHIP
ax2 = ax1.twinx()  
color2 = '#2ca02c'
ax2.set_ylabel('Twitch Avg Viewership', color=color2, fontsize=14, fontweight='bold')
ax2.fill_between(df['date'], df['ort_izleyici'], color=color2, alpha=0.15, label='Twitch Viewership')
sns.lineplot(data=df, x='date', y='ort_izleyici', ax=ax2, color=color2, alpha=0.5)
ax2.tick_params(axis='y', labelcolor=color2)

# TOURNAMENT SHADING (Visual highlighting loop)
for start, end, name, color, y_pos in turnuvalar:
    start_dt = pd.to_datetime(start)
    end_dt = pd.to_datetime(end)
    
    # Background shading (Higher alpha for Majors, lighter for S-Tier)
    alpha_val = 0.15 if color != 'gray' else 0.08
    ax1.axvspan(start_dt, end_dt, color=color, alpha=alpha_val)
    
    # Vertical text alignment for labels
    ax1.text(start_dt, ax1.get_ylim()[1] * y_pos, f' {name}', color=color if color != 'gray' else 'dimgray', 
             fontweight='bold', rotation=90, va='top', fontsize=10)

plt.title('CS2 Tier-1 Tournaments: Market Volatility vs Twitch Viewership (2023-2026)', fontsize=20, fontweight='bold')
fig.tight_layout()

# Save and Show Plot
plt.savefig('final_tournament_twitch_impact.png', dpi=300)
print("✅ PLOT SAVED as 'final_tournament_twitch_impact.png'!")
plt.show()