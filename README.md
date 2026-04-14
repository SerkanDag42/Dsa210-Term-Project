# CS2 Market Analysis & Viewership Correlation Project (DSA 210)

This project explores the correlation between Counter-Strike 2 in-game item prices and professional tournament viewership data (Twitch).

## 🚀 Analysis Workflow (Based on Course Guidelines)

### 1. Data Collection & Preprocessing
- **Steam Market Data:** Scraped ~200 Tier-1 skins and stickers using custom Python scripts (`import items.py`).
- **Twitch Data:** Integrated daily average viewership data for CS2.
- **Normalization:** Standardized date formats and handled missing values using forward-fill (ffill).

### 2. Exploratory Data Analysis (EDA)
- **Market Index:** Calculated the **Total Portfolio Value (Sum)** to represent overall market trends.
- **Event Mapping:** Visualized price fluctuations during 4 Major tournaments.
- **Visualization:** Dual-axis plots showing Price vs. Viewership (`final_tournament_twitch_impact.png`).

### 3. Hypothesis Testing
- **Pearson Correlation:** Tested the strength of the relationship between viewership spikes and price changes.
- **T-Test:** Compared market volatility during tournament periods vs. normal periods (P-Value < 0.05).

### 4. Machine Learning (Predictive Modeling)
- **Model:** Random Forest Regressor.
- **Goal:** Predicting the Total Portfolio Value based on viewership numbers and tournament status.
- **Performance:** High R-Squared accuracy, visualized via Actual vs. Predicted scatter plots.

