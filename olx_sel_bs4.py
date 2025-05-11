import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Setup
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

# Daftar URL Jabodetabek
urls = {
    "Jakarta Selatan": "https://www.olx.co.id/jakarta-selatan_g4000030/q-mobil",
    "Jakarta Utara": "https://www.olx.co.id/jakarta-utara_g4000029/q-mobil",
    "Jakarta Timur": "https://www.olx.co.id/jakarta-timur_g4000027/q-mobil",
    "Jakarta Barat": "https://www.olx.co.id/jakarta-barat_g4000026/q-mobil",
    "Jakarta Pusat": "https://www.olx.co.id/jakarta-pusat_g4000028/q-mobil",
    "Bekasi": "https://www.olx.co.id/kota-bekasi_g2000004/q-mobil",
    "Depok": "https://www.olx.co.id/kota-depok_g2000002/q-mobil",
    "Tangerang": "https://www.olx.co.id/kota-tangerang_g2000007/q-mobil",
    "Tangerang Selatan": "https://www.olx.co.id/tangerang-selatan-kota_g4000080/q-mobil",
    "Bogor": "https://www.olx.co.id/kota-bogor_g2000001/q-mobil"
}

# Final storage
all_products = []

# Loop tiap kota
for kota, url in urls.items():
    print(f"\nScraping {kota}...")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(2)

    click_count = 0
    for i in range(1000):
        time.sleep(2)
        try:
            driver.find_element(By.CSS_SELECTOR, "div._38O09 > button").click()
            click_count += 1
        except NoSuchElementException:
            print(f"Tidak ada tombol 'Load More' (diklik sebanyak {click_count} kali)")
            break

    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for item in soup.find_all('li', class_='_1DNjI'):
        nama = item.find('span', class_='_2poNJ')
        lokasi = item.find('span', class_='_2VQu4')
        tahun = item.find('span', class_='YBbhy')
        harga = item.find('span', class_='_2Ks63')
        gambar_tag = item.find('div', class_='_23Jeb')
        img_url = None
        if gambar_tag:
            img = gambar_tag.find('img')
            if img and img.get('src'):
                img_url = img['src']

        lokasi_text = lokasi.text.strip() if lokasi else 'N/A'
        kota = lokasi_text.split(',')[-1].strip() if ',' in lokasi_text else 'N/A'

        all_products.append((
            nama.text if nama else 'N/A',
            lokasi_text,
            tahun.text if tahun else 'N/A',
            harga.text if harga else 'N/A',
            kota,  # Simpan kota dari lokasi
            img_url if img_url else 'N/A'
    ))

    driver.quit()

# Simpan ke DataFrame
df = pd.DataFrame(all_products, columns=['Nama_Produk', 'Lokasi', 'Tahun', 'Price', 'Wilayah', 'Gambar_URL'])
print(df.info())

df.to_excel("data_mobil_terbaru.xlsx", index=False)
print("✅ Data berhasil disimpan ke data_mobil_jabodetabek.xlsx")
