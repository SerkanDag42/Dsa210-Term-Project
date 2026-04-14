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

# 1. ZENGİNLEŞTİRİLMİŞ VERİYİ YÜKLE
df = pd.read_csv("enriched_market_data.csv")
df['date'] = pd.to_datetime(df['date'])

# --- EKSİK OLAN MARKET_INDEX HESAPLAMASI BURAYA EKLENDİ ---
# Item sütunlarını bul (Tarih, Turnuva ve İzleyici dışındakiler)
item_columns = [col for col in df.columns if col not in ['date', 'Tournament', 'ort_izleyici', 'tarih']]
# Toplam Portföy Değerini (Sum) hesapla
df['Market_Index'] = df[item_columns].sum(axis=1)

# Eksik (NaN) izleyici verisi olan (mesela turnuvanın oynanmadığı boş günler) satırları temizle
df = df.dropna(subset=['Market_Index', 'ort_izleyici'])

print("="*60)
print("🏆 DSA 210 - FİNAL PROJESİ İSTATİSTİK VE ML RAPORU 🏆")
print("="*60)

# ==========================================
# ADIM 1: HİPOTEZ TESTİ (HYPOTHESIS TESTING)
# ==========================================
print("\n--- 1. HİPOTEZ TESTLERİ ---")

# Test 1: Pearson Korelasyonu (İzleyici vs Fiyat)
corr, p_value_corr = stats.pearsonr(df['ort_izleyici'], df['Market_Index'])
print(f"📌 Pearson Korelasyonu (r): {corr:.4f}")
print(f"   P-Value: {p_value_corr:.4e}")
if p_value_corr < 0.05:
    print("   👉 SONUÇ: P-Value < 0.05. H0 REDDEDİLDİ! İzleyici sayısı ile piyasa değeri arasında anlamlı bir ilişki var.")
else:
    print("   👉 SONUÇ: Anlamlı bir ilişki bulunamadı.")

# Test 2: T-Test (Turnuva Dönemi vs Normal Dönem)
tournament_prices = df[df['Tournament'] != 'Normal Period']['Market_Index']
normal_prices = df[df['Tournament'] == 'Normal Period']['Market_Index']

t_stat, p_value_t = stats.ttest_ind(tournament_prices, normal_prices, equal_var=False)
print(f"\n📌 T-Testi (Turnuva vs Normal Dönem Oynaklığı):")
print(f"   T-Statistik Değeri: {t_stat:.4f}")
print(f"   P-Value: {p_value_t:.4e}")
if p_value_t < 0.05:
    print("   👉 SONUÇ: P-Value < 0.05. H0 REDDEDİLDİ! Turnuva dönemlerindeki fiyatlar normal dönemlerden istatistiksel olarak farklıdır.")
else:
    print("   👉 SONUÇ: Turnuva dönemleri ile normal dönemler arasında anlamlı fiyat farkı yoktur.")

# ==========================================
# ADIM 2: MAKİNE ÖĞRENMESİ (RANDOM FOREST)
# ==========================================
print("\n--- 2. MAKİNE ÖĞRENMESİ (PREDICTIVE MODELING) ---")

# Makine turnuva isimlerini (Yazı) anlayabilsin diye One-Hot Encoding yapıyoruz
X = pd.get_dummies(df[['ort_izleyici', 'Tournament']], drop_first=True)
y = df['Market_Index']

# Train-Test Split (%80 Eğitim, %20 Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Random Forest Modeli
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Tahmin
y_pred = rf_model.predict(X_test)

# Metrikler
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print(f"📌 Model Başarısı (R-Squared): {r2:.4f} (Fiyatlardaki değişimin %{r2*100:.1f}'ini açıklıyor)")
print(f"📌 Ortalama Mutlak Hata (MAE): ${mae:.2f}")

# ==========================================
# ADIM 3: ML GRAFİKLERİ
# ==========================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))

# Grafik 1: Gerçek vs Tahmin
sns.scatterplot(x=y_test, y=y_pred, alpha=0.7, color='purple', ax=ax1)
ax1.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2) 
ax1.set_title('Random Forest: Actual vs Predicted Portfolio Value', fontweight='bold')
ax1.set_xlabel('Actual Portfolio Value ($)', fontweight='bold')
ax1.set_ylabel('Predicted Portfolio Value ($)', fontweight='bold')

# Grafik 2: Değişken Önemi (Feature Importance)
feature_importances = pd.Series(rf_model.feature_importances_, index=X.columns).sort_values(ascending=False)
sns.barplot(x=feature_importances.values, y=feature_importances.index, palette='viridis', ax=ax2)
ax2.set_title('What Drives the Market? (Feature Importance)', fontweight='bold')
ax2.set_xlabel('Importance Score', fontweight='bold')

plt.tight_layout()
plt.savefig('ml_analysis_results.png', dpi=300)
print("\n✅ Grafikler 'ml_analysis_results.png' olarak kaydedildi!")
print("="*60)
plt.show()