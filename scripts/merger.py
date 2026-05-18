import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

# 1. LOAD DATA 
csv_file = "data/raw/dsa210_mega_data.csv" 
twitch_file = "data/raw/cs2_gunluk_izleyici.csv"
tourney_file = "data/raw/tournaments.csv"

print("1. Loading datasets...")
try:
    df_market = pd.read_csv(csv_file)
    df_twitch = pd.read_csv(twitch_file)
    df_tournaments = pd.read_csv(tourney_file)
except FileNotFoundError as e:
    print(f"ERROR: File not found! {e}")
    exit()

df_twitch.rename(columns={'tarih': 'date', 'ort_izleyici': 'avg_viewer'}, inplace=True)

df_market['date'] = pd.to_datetime(df_market['date'])
df_twitch['date'] = pd.to_datetime(df_twitch['date']).dt.tz_localize(None).dt.normalize()
df_tournaments['start_date'] = pd.to_datetime(df_tournaments['start_date'])
df_tournaments['end_date'] = pd.to_datetime(df_tournaments['end_date'])

df = pd.merge(df_market, df_twitch[['date', 'avg_viewer']], on='date', how='left')

# 2. PRO TOURNAMENT CALENDAR (DATA ENRICHMENT)
print("2. Processing Tournament Calendar dynamically from CSV...")

# Function for tournament labeling directly from DataFrame
def get_tournament_name(date_val):
    for _, row in df_tournaments.iterrows():
        if row['start_date'] <= date_val <= row['end_date']:
            return row['tournament_name']
    return 'Normal Period'

df['Tournament'] = df['date'].apply(get_tournament_name)

os.makedirs("data/processed", exist_ok=True)
enriched_file = "data/processed/enriched_market_data.csv"
df.to_csv(enriched_file, index=False)
print(f"✅ Table enriched: '{enriched_file}' is ready.")
print("-" * 60)

# 3. DUAL-AXIS EXPLORATORY DATA ANALYSIS (EDA)
print("3. Generating Dual-Axis EDA Plot...")

# TOTAL PORTFOLIO VALUE (SUM)
item_columns = [col for col in df.columns if col not in ['date', 'Tournament', 'avg_viewer']]
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
ax2.fill_between(df['date'], df['avg_viewer'], color=color2, alpha=0.15, label='Twitch Viewership')
sns.lineplot(data=df, x='date', y='avg_viewer', ax=ax2, color=color2, alpha=0.5)
ax2.tick_params(axis='y', labelcolor=color2)

# DYNAMIC TOURNAMENT SHADING FROM CSV
major_colors = ['cyan', 'orange', 'red', 'purple', 'magenta', 'blue']
major_idx = 0

for _, row in df_tournaments.iterrows():
    start_dt = row['start_date']
    end_dt = row['end_date']
    name = row['tournament_name']
    tier = row['tournament_type']
    
    # Assign styling based on Tier dynamically
    if tier == 'Major':
        color = major_colors[major_idx % len(major_colors)]
        major_idx += 1
        alpha_val = 0.15
        text_color = color
        y_pos = 0.95
    else: # S-Tier
        color = 'gray'
        alpha_val = 0.08
        text_color = 'dimgray'
        y_pos = 0.85
        
    ax1.axvspan(start_dt, end_dt, color=color, alpha=alpha_val)
    ax1.text(start_dt, ax1.get_ylim()[1] * y_pos, f' {name}', color=text_color, 
             fontweight='bold', rotation=90, va='top', fontsize=10)

plt.title('CS2 Tier-1 Tournaments: Market Volatility vs Twitch Viewership (2023-2026)', fontsize=20, fontweight='bold')
fig.tight_layout()

os.makedirs("results", exist_ok=True)
plot_path = "results/final_tournament_twitch_impact.png"
plt.savefig(plot_path, dpi=300)
print(f"✅ PLOT SAVED as '{plot_path}'!")
plt.show()