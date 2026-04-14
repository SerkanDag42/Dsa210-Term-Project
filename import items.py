import requests
import pandas as pd
import time
import urllib.parse
import re
import json
import os
from datetime import datetime

# Dosya yolları
TXT_FILE = "itemler.txt"
CSV_FILE = "dsa210_mega_data.csv"

# TXT dosyasını oku
if not os.path.exists(TXT_FILE):
    print(f"HATA: {TXT_FILE} bulunamadı. Lütfen listeyi oluşturun.")
    exit()

with open(TXT_FILE, "r", encoding="utf-8") as f:
    # Boşlukları temizle ve boş satırları at
    items_to_track = [line.strip() for line in f.readlines() if line.strip()]

master_df = pd.DataFrame()

# Eğer eski verimiz varsa yükle (Kaldığı yerden devam etme mantığı)
if os.path.exists(CSV_FILE):
    master_df = pd.read_csv(CSV_FILE)
    master_df['date'] = pd.to_datetime(master_df['date'])
    existing_items = master_df.columns.tolist()
    
    # Zaten indirilmiş olanları listeden çıkar
    items_to_track = [item for item in items_to_track if item not in existing_items]
    print(f"✅ CSV dosyası bulundu! Zaten inmiş olan itemler es geçilecek.")

print(f"🚀 MEGA OPERASYON: Çekilecek {len(items_to_track)} yeni item bulundu!")
print("-" * 60)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

for index, item in enumerate(items_to_track):
    print(f"[{index+1}/{len(items_to_track)}] Çekiliyor: {item}")
    
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
                    
                    # 2023 sonrası (CS2 Odaklı)
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
                    
                    # Her itemden sonra kaydet
                    save_df = master_df.sort_values('date').ffill()
                    try:
                        save_df.to_csv(CSV_FILE, index=False)
                        print(f"  -> Başarılı! {item} CSV'ye yazıldı.")
                    except PermissionError:
                        print("  -> DİKKAT: CSV açık. Kapatırsan bir sonrakinde yazılacak.")
                else:
                    print(f"  -> Es geçildi: 2023 sonrasında veri yok.")
            else:
                print("  -> Hata: İsim yanlış olabilir veya satılmıyor.")
        
        elif response.status_code == 429:
            print("  -> DİKKAT (429): Steam 'Biraz dur' dedi. KOD DURDURULDU.")
            print(f"  -> {CSV_FILE} güvende. 10-15 dk bekle, sonra kodu tekrar çalıştır.")
            print("  -> Zaten inenleri otomatik atlayıp kaldığı yerden devam edecek!")
            break
        else:
            print(f"  -> Hata kodu: {response.status_code}")
            
    except Exception as e:
        print(f"  -> Beklenmedik hata (Atlandı): {e}")
    
    # Steam'i üzmemek için 18 saniye uyku
    if index < len(items_to_track) - 1:
        time.sleep(18)

print("-" * 60)
print(f"🎉 İŞLEM DURDU VEYA BİTTİ. Güncel dosya: {CSV_FILE}")