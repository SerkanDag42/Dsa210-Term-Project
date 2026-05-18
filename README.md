# 📈 Counter-Strike 2 Marketplace & Esports Viewership Dynamics
### 📊 DSA 210 - Introduction to Data Science Final Term Project

**University:** Sabancı University  
**Course:** DSA 210 - Introduction to Data Science  
**Student:** Serkan Dağ  
**Academic Semester:** Spring 2026  

---

## 📌 Project Overview
This project explores the macroeconomic relationship between Counter-Strike 2 (CS2) professional esports viewership data on Twitch and the internal digital asset market on Steam. The main objective is to analyze whether community engagement spikes inject structural changes into item prices, categorize the market into autonomous economic states, and test the predictability of a digital commodity market using external social interest parameters and advanced time-series forecasting.

---

## 📂 Repository Components & File Structure

The repository is organized following industry-standard data science project structures to ensure absolute reproducibility, clean path management, and separation of concerns.

```text
dsa210/
├── data/
│   ├── raw/                           # Raw datasets collected via APIs & scrapers
│   │   ├── itemler.txt                # Target skin list for tracking
│   │   ├── liquipedia.html            # Stored offline archive for tournament scraping
│   │   ├── tournaments.csv            # Extracted tournament schedules
│   │   ├── cs2_gunluk_izleyici.csv    # Historical Twitch daily average viewership
│   │   └── dsa210_mega_data.csv       # Extracted daily Steam market prices
│   └── processed/                     # Enriched data ready for modeling
│       └── enriched_market_data.csv   # Merged and normalized analytical master matrix
├── notebooks/                         # Core research and visualization environments
│   ├── 1_EDA_and_Hypothesis.ipynb     # Statistical testing & dual-axis timeline research
│   └── 2_ML_Modeling.ipynb            # Unsupervised clustering, Random Forest, & ARIMAX
├── scripts/                           # Production-ready Python automation modules
│   ├── import_items.py                # Steam Community Market API scraping engine
│   ├── scrape_tournaments.py          # BeautifulSoup engine parsing local Liquipedia HTML
│   ├── final_analysis.py              # Standalone statistical summary and reporting script
│   └── merger.py                      # Data pipeline utility aligning timelines
├── results/                           # Permanent evaluation assets and plot exports
│   ├── final_tournament_twitch_impact.png   # Dual-axis overlay timeline plot
│   ├── kmeans_evaluation_professional.png  # Elbow and Silhouette validation plots
│   ├── kmeans_evaluation.png               # Final K-Means cluster partition scatter plot
│   ├── ml_analysis_results.png             # Supervised regression actual-vs-predicted plot
│   └── arimax_market_forecast.png          # ARIMAX sequential time-series projection plot
├── index.html                         # Interactive visual portfolio web dashboard (SPA)
├── Dsa 210 Final Report.pdf           # Comprehensive formal academic final report
└── requirements.txt                   # Environment dependencies blueprint

## 🚀 Analytical Architecture & Methodology

### Phase 1: Exploratory Data Analysis & Classical Hypotheses
* **The Market Index Framework:** Individual skin prices were mathematically consolidated into an aggregated **Total Market Value** index to capture underlying macroeconomic movements rather than individual product anomalies.
* **Pearson Correlation Analysis:** Isolated a statistically significant but low linear dependency (**r = 0.0717, p < 0.05**) between daily Twitch audience crowds and pricing indexes, indicating speculative lags rather than immediate price reactions.
* **Independent Two-Sample T-Test:** Evaluated asset volatility across segmented calendar blocks (Esports Tournament Windows vs. Regular Periods). The null hypothesis was strongly rejected (**p < 0.05**), proving that tournament environments systematically disrupt baseline market indices.
* **One-Way ANOVA Framework:** Checked whether separate competitive tiers (Valve-sponsored Majors vs. Independent S-Tier brackets) execute varying economic weights. The test yielded extreme statistical significance (**p = 1.41e-13**), confirming that in-game economic drops unique to Majors act as severe market catalysts.

### Phase 2: Unsupervised Learning (Market State Clustering)
To uncover the structural boundaries hidden within market fluctuations, we implemented **K-Means Clustering (k = 3)**:
* Features were standardized using a `StandardScaler` layer following log-transformations to control high data skewness.
* Bounded by a stable silhouette coefficient (**0.464**), the model autonomously mapped out three operational states:
  * **Stagnant Market:** Low viewership activity matched with baseline, horizontal commodity indices.
  * **Transition Nodes:** Intermediate boundaries showcasing pricing stickiness and transaction delays.
  * **Hype Market:** Explosive tournament stream volumes actively driving vertical market index expansions.

### Phase 3: Supervised Learning (Predictive Regression Bounding)
We benchmarked multi-model regression architectures—**Linear Regression, Optimized KNN (GridSearchCV bounded), Random Forest, and Gradient Boosting**—to map asset value variance:
* **The Predictive Ceiling (R² ≈ 0):** Traditional cross-validation models yielded predictive performance close to zero. In quantitative finance, this matches the **Random Walk Hypothesis**, verifying that predicting continuous specific pricing points using only platform daily crowd logs remains heavily bounded by market efficiency.
* **Feature Importance Profiling:** Node-split analytics inside the Gradient Boosting pipeline confirmed our core domain assumption; daily Twitch stream metrics (`avg_viewer`) secured over **80%** of the model importance score, making it the absolute dominant external force driving market variance.

### Phase 4: Sequential Time-Series Forecasting (ARIMAX)
To address the chronological limitations of standard machine learning, we deployed an **ARIMAX(1,1,1) Model**:
* The time-series framework integrates the natural chronological momentum of the price index (Autoregressive dependencies) while evaluating `avg_viewer` and `Tournament` variables as external exogenous shocks.
* The out-of-sample forecast yielded a negative **R²** score accompanied by a mean-reverting path wrapped inside expanding confidence fields. This provides empirical proof of the **Efficient Market Hypothesis (EMH)**; external platform hype shocks are instantly priced into the digital commodities, preventing long-term directional arbitrage.

---

## 🤖 AI Collaboration & Disclosure Statement
In accordance with modern research frameworks, this project was developed in an agile co-pilot relationship with **Google Gemini (Advanced Tier / Gemini Pro Architecture)**.

Artificial intelligence was structurally utilized for the following core engineering and analytical milestones:
* **Data Pipeline Refactoring:** Optimizing absolute-to-relative path execution schemes across local VS Code terminal environments and Jupyter Notebook working directories to guarantee zero-configuration execution.
* **Statistical Modeling Architecture:** Formulating state-space wrappers for the implementation of the `SARIMAX` time-series modules via `statsmodels` and mapping mathematical code logic into formal economic commentary.
* **Web Dashboard Optimization:** Adapting CSS3 styling layers and scaling data arrays within the dynamic Chart.js module inside the `index.html` SPA dashboard.

All theoretical interpretations, analytical designs, final report syntheses, and academic ownership remain fully maintained by the human author.

---

## 🏷️ Versioning & Delivery
Final release submission configured for **Sabancı University DSA 210 Term Project Final Delivery Requirements**.