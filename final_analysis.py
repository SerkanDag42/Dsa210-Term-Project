import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

# 1. LOAD ENRICHED DATA
df = pd.read_csv("enriched_market_data.csv")
df['date'] = pd.to_datetime(df['date'])

# --- ADD MISSING MARKET_INDEX CALCULATION HERE ---
# Find item columns (excluding date, Tournament, viewership, and tarih)
item_columns = [col for col in df.columns if col not in ['date', 'Tournament', 'ort_izleyici', 'tarih']]
# Calculate Total Portfolio Value (Sum)
df['Market_Index'] = df[item_columns].sum(axis=1)

# Clean rows with missing (NaN) viewership data (e.g., empty days with no tournament matches)
df = df.dropna(subset=['Market_Index', 'ort_izleyici'])

print("="*60)
print("🏆 DSA 210 - FINAL PROJECT STATISTICS AND ML REPORT 🏆")
print("="*60)

# ==========================================
# STEP 1: HYPOTHESIS TESTING
# ==========================================
print("\n--- 1. HYPOTHESIS TESTS ---")

# Test 1: Pearson Correlation (Viewership vs Price)
corr, p_value_corr = stats.pearsonr(df['ort_izleyici'], df['Market_Index'])
print(f"📌 Pearson Correlation (r): {corr:.4f}")
print(f"   P-Value: {p_value_corr:.4e}")
if p_value_corr < 0.05:
    print("   👉 RESULT: P-Value < 0.05. H0 REJECTED! There is a significant relationship between viewership count and market value.")
else:
    print("   👉 RESULT: No significant relationship found.")

# Test 2: T-Test (Tournament Period vs Normal Period Volatility)
tournament_prices = df[df['Tournament'] != 'Normal Period']['Market_Index']
normal_prices = df[df['Tournament'] == 'Normal Period']['Market_Index']

t_stat, p_value_t = stats.ttest_ind(tournament_prices, normal_prices, equal_var=False)
print(f"\n📌 T-Test (Tournament vs Normal Period Volatility):")
print(f"   T-Statistic Value: {t_stat:.4f}")
print(f"   P-Value: {p_value_t:.4e}")
if p_value_t < 0.05:
    print("   👉 RESULT: P-Value < 0.05. H0 REJECTED! Prices during tournament periods are statistically different from normal periods.")
else:
    print("   👉 RESULT: No significant price difference between tournament and normal periods.")

# ==========================================
# STEP 2: MACHINE LEARNING (RANDOM FOREST)
# ==========================================
print("\n--- 2. MACHINE LEARNING (PREDICTIVE MODELING) ---")

# Applying One-Hot Encoding so the machine can understand tournament names (string data)
X = pd.get_dummies(df[['ort_izleyici', 'Tournament']], drop_first=True)
y = df['Market_Index']

# Train-Test Split (80% Training, 20% Testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Random Forest Model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Prediction
y_pred = rf_model.predict(X_test)

# Metrics
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print(f"📌 Model Performance (R-Squared): {r2:.4f} (Explains {r2*100:.1f}% of the variance in prices)")
print(f"📌 Mean Absolute Error (MAE): ${mae:.2f}")

# ==========================================
# STEP 3: ML PLOTS
# ==========================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))

# Plot 1: Actual vs Predicted
sns.scatterplot(x=y_test, y=y_pred, alpha=0.7, color='purple', ax=ax1)
ax1.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2) 
ax1.set_title('Random Forest: Actual vs Predicted Portfolio Value', fontweight='bold')
ax1.set_xlabel('Actual Portfolio Value ($)', fontweight='bold')
ax1.set_ylabel('Predicted Portfolio Value ($)', fontweight='bold')

# Plot 2: Feature Importance
feature_importances = pd.Series(rf_model.feature_importances_, index=X.columns).sort_values(ascending=False)
sns.barplot(x=feature_importances.values, y=feature_importances.index, palette='viridis', ax=ax2)
ax2.set_title('What Drives the Market? (Feature Importance)', fontweight='bold')
ax2.set_xlabel('Importance Score', fontweight='bold')

plt.tight_layout()
plt.savefig('ml_analysis_results.png', dpi=300)
print("\n✅ Plots saved as 'ml_analysis_results.png'!")
print("="*60)
plt.show()