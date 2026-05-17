# 📈 Counter-Strike 2 Marketplace & Esports Viewership Dynamics
### 📊 DSA 210 - Introduction to Data Science Final Term Project

**University:** Sabancı University  
**Course:** DSA 210 - Introduction to Data Science  
**Student:** Serkan Dağ  
**Academic Semester:** Spring 2026  

---

## 📌 Project Overview
This project explores the macroeconomic relationship between Counter-Strike 2 (CS2) professional esports viewership data on Twitch and the internal digital asset market on Steam. The main objective is to analyze whether community engagement spikes inject structural changes into item prices, categorize the market into autonomous economic states, and test the predictability of a digital commodity market using external social interest parameters.

---

## 📂 Repository Components & File Structure

All project files are maintained directly in the root directory for absolute configuration stability. Below is a complete guide to the repository components:

### 1. Data Collection & Scraping Engine
* `itemler.txt`: Source catalog text file containing the selected list of high-tier CS2 skins and stickers analyzed.
* `import items.py`: Custom pipeline script pulling historical live market data from the Steam Community Market API.
* `scrape_tournaments.py`: Core web-scraping script built with BeautifulSoup that successfully targets local Liquipedia architecture to harvest major esports event timelines without network firewalls.
* `merger.py`: Data engineering utility aligning independent timelines by synchronizing market indices and stream counts.
* `scrape_twitch_viewership.py`: Python pipeline script designed to handle external API streams or dynamically reconstruct historical Twitch viewership data to ensure total pipeline autonomy.

### 2. Operational Datasets
* `liquipedia.html`: The captured local HTML source file representing the S-Tier tournament database from Liquipedia.
* `tournaments.csv`: The clean, structured calendar dataset extracted by our scraper containing start dates, end dates, names, and tiers of events.
* `cs2_gunluk_izleyici.csv`: Daily historical time-series dataset containing average Twitch streaming metrics for CS2.
* `dsa210_mega_data.csv`: Aggregated transaction value matrix holding historical daily asset values for indexed weapon skins.
* `enriched_market_data.csv` : Normalized and merged operational datasets prepared dynamically for statistical models.


### 3. Comprehensive Analysis Notebooks
* `1_EDA_and_Hypothesis.ipynb`: **Core Statistical Hub.** Contains data parsing, baseline indexing, and standard curriculum hypothesis tests (Pearson, T-Test, and ANOVA).
* `2_ML_Modeling.ipynb`: **Core Modeling Hub.** Implements unsupervised K-Means structural segmentation and supervised multi-model regression architectures.
* `DSA210_CS2_Analysis_Report.ipynb` & `knn.ipynb`: Supplementary environment logs and initial development scratchpads.

### 4. Empirical Result Plots
* `final_tournament_twitch_impact.png`: Dual-axis visualization illustrating matching trends between tournament dates, stream spikes, and overall market expansion.
* `cs2_kmeans_market_states.png` & `kmeans_evaluation_professional.png`: Visualization output mapping macro market clustering boundaries.
* `ml_final_strict_hypothesis.png`: Final validation chart pairing comparative cross-model evaluation grids alongside empirical feature weights.

---

## 🚀 Analytical Architecture & Methodology

### Phase 1: Exploratory Data Analysis & Classical Hypotheses
1. **The Market Index Framework:** Individual skin prices were mathematically aggregated into a composite **Total Market Value** index to capture underlying macroeconomic trends rather than independent product variance.
2. **Pearson Correlation Check:** Evaluated the linear overlap between raw platform viewership metrics and pricing scales. Results yielded a statistically significant but low linear dependency, pointing toward speculative delays rather than immediate reactions.
3. **Independent Two-Sample T-Test:** Evaluated the market value distributions by segmenting active tournament days against standard regular days. The null hypothesis was strongly rejected ($p < 0.05$), proving that competitive windows systematically shift item pricing baselines.
4. **One-Way ANOVA Framework:** Checked whether separate tournament tiers (Valve-sponsored Majors vs. independent S-Tier events) impact asset valuation differently. The variance test proved that varying tournament tiers create distinct financial shocks inside the ecosystem.

### Phase 2: Unsupervised Learning (Market State Clustering)
To extract clean structural behaviors from highly fluctuating economic periods, we applied an unsupervised framework using **K-Means Clustering ($k=3$)**:
* Raw financial inputs were standardized using a `StandardScaler` after processing log-transformations to handle severe data skewness.
* The model autonomously partitioned the CS2 marketplace grid into 3 macro states with a robust silhouette efficiency check ($0.464$):
  1. *Stagnant Market:* Lower baseline community interaction paired with standard baseline asset indices.
  2. *Transition Phase:* Intermediate points showcasing pricing stickiness and transaction delays.
  3. *Hype Market:* Explosive tournament streaming volumes driving market expansion.

### Phase 3: Supervised Learning (Predictive Modeling Framework)
We benchmarked four regression algorithms—**Linear Regression**, **Optimized KNN Regressor** (tuned via `GridSearchCV` bounding), **Random Forest**, and **Gradient Boosting**—using an 80/20 train-test split pattern:
* **The Predictive Reality ($R^2 \approx 0$):** Cross-validation metrics resulted in baseline $R^2$ tracking close to zero across independent parameters. In quantitative finance, this matches the **Random Walk Hypothesis**. This outcome confirms our pipeline is completely free of **Target Leakage**; predicting precise asset values using only basic daily crowd volume is bounded by market efficiency.
* **Feature Importance Profiling:** Despite low predictive linearity, isolating node-split ratios inside the Gradient Boosting framework provided clear confirmation of our primary assumption. Daily streaming crowd volume (`ort_izleyici`) holds over **80%** of the feature importance score, proving it is the single most dominant external factor guiding virtual asset market fluctuations.

---

## 🏷️ Versioning
Final release submission configured for **DSA 210 Term Project Final Delivery**.