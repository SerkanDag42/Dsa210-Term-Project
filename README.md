# 📈 CS2 Market Analysis & Viewership Correlation Project

**University:** Sabancı University  
**Course:** DSA 210 - Introduction to Data Science  
**Student:** Serkan Dağ  
**Semester:** Term Project

---

## 📌 Project Overview
This project investigates the macroeconomic relationship between Counter-Strike 2 (CS2) professional e-sports viewership on Twitch and the in-game cosmetic item economy. The main objective is to understand if and how attention metrics (viewers) inject volatility into digital item prices, and whether we can categorize the market into distinct economic states.

## 📂 Project Directory Structure

Here is a breakdown of the files included in this repository and their purposes:

### 1. Data Collection & Processing Scripts
*   `itemler.txt`: Contains the list of targeted Tier-1 CS2 items (skins/stickers) for the analysis.
*   `import items.py`: Custom Python scraper/API script used to fetch historical price data from the Steam Community Market.
*   `merger.py`: Data engineering script used to clean and merge raw market data with the viewership data.
*   `final_analysis.py`: Contains the standalone Python code for statistical hypothesis testing and Machine Learning models.

### 2. Datasets
*   `cs2_gunluk_izleyici.csv`: Raw dataset containing daily average Twitch viewership for CS2.
*   `dsa210_mega_data.csv`: Raw aggregated market dataset containing daily prices of the scraped CS2 items.
*   `enriched_market_data.csv`: The final, preprocessed, and merged dataset ready for EDA and Machine Learning.

### 3. Notebooks (The Core Analysis)
*   `DSA210_CS2_Analysis_Report.ipynb`: **The main Jupyter Notebook.** This file contains the entire pipeline end-to-end (EDA, Hypothesis Testing, Random Forest, and K-Means Clustering) along with analytical commentary. *(Please review this file for the complete project narrative).*
*   `ml.ipynb`: A supplementary scratchpad notebook used during the development of the ML models.

### 4. Output Visualizations
*   `final_tournament_twitch_impact.png`: Dual-axis EDA chart showing the visual correlation between Major tournaments, viewership spikes, and portfolio value.
*   `ml_analysis_results.png`: Visual outputs of the Random Forest Regressor and Feature Importance analysis.
*   `cs2_kmeans_market_states.png`: The final scatter plot from Milestone 2 showing the K-Means clustered market states.

---

## 🚀 Analysis Workflow & Methodology

### Milestone 1: EDA, Hypothesis Testing & Supervised Learning
**1. Exploratory Data Analysis (EDA)**
- **Market Index:** Calculated the **Total Portfolio Value (Sum)** to represent overall macroeconomic trends.
- **Visual Correlation:** Created a dual-axis plot (`final_tournament_twitch_impact.png`) visually suggesting that massive viewership spikes align with market inflation.

**2. Statistical Hypothesis Testing**
- **Pearson Correlation Test:** Proved a statistically significant but non-linear relationship between viewership and market value ($p < 0.05$, $r = 0.0717$). 
- **Two-Sample T-Test:** Definitively proved that market volatility during tournament periods is statistically different (higher) than in normal periods.

**3. Predictive Modeling (Supervised Learning)**
- We trained a **Random Forest Regressor** to predict exact market values based on viewership and tournament flags.
- **Finding:** The model yielded a negative R-Squared ($-0.1859$). This was a crucial analytical finding: the CS2 economy has internal momentum, speculative delays, and price stickiness. It cannot be linearly predicted *just* by counting viewers. **This specific predictive limitation laid the exact groundwork and justification for Milestone 2.**

### Milestone 2: Market State Clustering (Unsupervised Learning)
To address the predictive limitations found in Milestone 1, we pivoted our methodology to Unsupervised Learning. Instead of trying to predict the *exact price*, we aimed to understand the *macro-behavior* of the market.

- **K-Means Clustering:** Applied K-Means ($K=3$) using `StandardScaler` to normalize viewership and price magnitudes.
- **Conclusion:** The algorithm successfully and autonomously categorized the CS2 economy into three distinct states with a solid Silhouette Score ($0.464$):
  1. **Hype Market** (Peak Viewers / Inflated Price)
  2. **Transition / Anomaly Period** (Transition phases showing price stickiness)
  3. **Stagnant Market** (Low Viewers / Baseline Price)
- **Final Insight:** While predicting exact daily prices is highly complex, the overarching macro-states of the game's economy are demonstrably driven by e-sports attention.

---

## 🏷️ Versioning
Final submission is tagged as **Milestone 2 (Final Term Project)**.