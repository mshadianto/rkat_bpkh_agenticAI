# 🔍 Panduan Web Scraper Bank Muamalat

Panduan lengkap untuk menggunakan web scraper yang etis dan legal untuk mengumpulkan data publik dari website Bank Muamalat.

## ⚖️ DISCLAIMER PENTING

**🚨 PERINGATAN LEGAL:**
- Scraper ini HANYA mengambil data yang **dipublikasikan secara umum**
- TIDAK mengakses data privasi nasabah atau data internal
- Menghormati robots.txt dan terms of service website
- Menggunakan rate limiting untuk tidak membebani server
- **Gunakan dengan tanggung jawab dan sesuai hukum yang berlaku**

## 📋 Prerequisites

### 1. Install Dependencies
```bash
pip install requests beautifulsoup4 pandas lxml
```

### 2. Check Legal Compliance
```bash
# Cek robots.txt Bank Muamalat
curl https://www.bankmuamalat.co.id/robots.txt
```

## 🚀 Quick Start

### 1. Jalankan Scraper Dasar
```python
from bank_muamalat_scraper import BankMuamalatScraper

# Inisialisasi scraper dengan delay 2 detik
scraper = BankMuamalatScraper(delay=2.0)

# Jalankan scraping komprehensif
results = scraper.run_comprehensive_scrape()

# Simpan hasil
filename = scraper.save_results(results)
print(f"Data tersimpan di: {filename}")
```

### 2. Jalankan dari Command Line
```bash
python bank_muamalat_scraper.py
```

## 📊 Data yang Dapat Di-scrape

### ✅ Data LEGAL untuk di-scrape:

#### 1. **Informasi Perusahaan**
- Profil perusahaan publik
- Kontak dan alamat yang dipublikasikan
- Sejarah perusahaan
- Struktur organisasi publik

#### 2. **Berita & Pengumuman**
- Siaran pers
- Pengumuman publik
- Berita perusahaan
- Update korporat

#### 3. **Laporan Keuangan**
- Link ke laporan tahunan
- Laporan kuartalan yang dipublikasikan
- Investor relations materials
- Prospektus yang tersedia publik

#### 4. **Produk & Layanan**
- Informasi produk publik
- Deskripsi layanan
- Tarif dan syarat yang dipublikasikan
- Brosur produk

### ❌ Data yang TIDAK BOLEH di-scrape:

- 🚫 Data nasabah atau informasi pribadi
- 🚫 Data di balik login/password
- 🚫 Informasi internal confidential
- 🚫 Database transaksi
- 🚫 Sistem internal banking
- 🚫 Data yang melanggar ToS

## 🛠️ Konfigurasi Scraper

### 1. Basic Configuration
```python
scraper = BankMuamalatScraper(
    delay=2.0,  # Delay 2 detik antar request
)
```

### 2. Advanced Configuration
```python
# Custom headers
scraper.session.headers.update({
    'User-Agent': 'YourCompany Research Bot 1.0',
    'From': 'research@yourcompany.com'  # Email kontak
})

# Set timeout
scraper.session.timeout = 30
```

### 3. Respectful Scraping Settings
```python
# Delay yang disarankan berdasarkan beban server
DELAY_SETTINGS = {
    'conservative': 5.0,  # 5 detik (paling aman)
    'moderate': 2.0,      # 2 detik (balanced)
    'aggressive': 1.0     # 1 detik (gunakan hati-hati)
}
```

## 📈 Integrasi dengan Dashboard

### 1. Update main.py untuk Real Data
```python
# Tambahkan import di main.py
from data_integration import BankMuamalatDataIntegrator, show_real_data_dashboard

# Tambahkan menu baru di sidebar
if page == "🔍 Real Data":
    show_dashboard()
    show_real_data_dashboard()
```

### 2. Scheduled Data Refresh
```python
import schedule
import time

def auto_scrape():
    scraper = BankMuamalatScraper(delay=3.0)
    results = scraper.run_comprehensive_scrape()
    scraper.save_results(results)

# Schedule scraping setiap hari jam 6 pagi
schedule.every().day.at("06:00").do(auto_scrape)

while True:
    schedule.run_pending()
    time.sleep(3600)  # Check setiap jam
```

## 📊 Struktur Data Output

### 1. Company Information
```json
{
  "company_info": {
    "page_title": "Bank Muamalat Indonesia",
    "description": "Bank Syariah pertama di Indonesia...",
    "phone_numbers": ["+62-21-251-1411"],
    "emails": ["info@bankmuamalat.co.id"],
    "potential_address": "Jakarta, Indonesia"
  }
}
```

### 2. News & Announcements
```json
{
  "news": [
    {
      "title": "Bank Muamalat Luncurkan Produk Baru",
      "summary": "Bank Muamalat memperkenalkan...",
      "date_text": "15 Juli 2024",
      "link": "https://www.bankmuamalat.co.id/news/..."
    }
  ]
}
```

### 3. Financial Reports
```json
{
  "financial_reports": [
    {
      "title": "Laporan Tahunan 2023",
      "url": "https://www.bankmuamalat.co.id/reports/annual-2023.pdf",
      "type": "PDF"
    }
  ]
}
```

## 🔒 Best Practices Keamanan

### 1. Rate Limiting
```python
# Implementasi backoff strategy
import time
import random

def respectful_delay():
    base_delay = 2.0
    jitter = random.uniform(0.5, 1.5)
    time.sleep(base_delay + jitter)
```

### 2. Error Handling
```python
def safe_scrape(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = scraper.respectful_get(url)
            return response
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(5 * (attempt + 1))  # Exponential backoff
    return None
```

### 3. Monitoring & Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
```

## 📅 Jadwal Scraping yang Disarankan

### 1. Frequency Guidelines
```python
SCRAPING_SCHEDULE = {
    'news': 'daily',           # Berita setiap hari
    'financial_reports': 'weekly',  # Laporan seminggu sekali
    'company_info': 'monthly',      # Info perusahaan sebulan sekali
    'products': 'weekly'            # Produk seminggu sekali
}
```

### 2. Time Scheduling
```python
# Waktu optimal untuk scraping (server load rendah)
OPTIMAL_TIMES = [
    "02:00",  # Dini hari
    "06:00",  # Pagi
    "14:00",  # Siang
    "22:00"   # Malam
]
```

## 🚨 Error Handling & Troubleshooting

### 1. Common Issues

#### HTTP 403 Forbidden
```python
# Solusi: Update User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
```

#### Connection Timeout
```python
# Solusi: Increase timeout dan retry
session.timeout = 30
max_retries = 3
```

#### Rate Limited
```python
# Solusi: Increase delay
scraper = BankMuamalatScraper(delay=5.0)  # Increase to 5 seconds
```

### 2. Monitoring Script Health
```python
def health_check():
    try:
        response = requests.get('https://www.bankmuamalat.co.id', timeout=10)
        return response.status_code == 200
    except:
        return False

if not health_check():
    print("❌ Website tidak dapat diakses")
    exit(1)
```

## 📈 Performance Optimization

### 1. Caching Strategy
```python
import requests_cache

# Cache responses untuk 1 jam
session = requests_cache.CachedSession('bank_muamalat_cache', expire_after=3600)
```

### 2. Parallel Processing
```python
from concurrent.futures import ThreadPoolExecutor
import threading

def scrape_url(url):
    # Rate limit per thread
    with threading.Lock():
        time.sleep(2)
    return scraper.respectful_get(url)

# Max 2 concurrent threads (conservative)
with ThreadPoolExecutor(max_workers=2) as executor:
    futures = [executor.submit(scrape_url, url) for url in urls]
```

## 🔄 Integration Examples

### 1. Update Dashboard Metrics
```python
def update_dashboard_with_real_data():
    integrator = BankMuamalatDataIntegrator('latest_data.json')
    
    # Get real financial context
    metrics = integrator.extract_financial_metrics()
    
    # Update dashboard
    st.metric("News Sentiment", metrics['news_sentiment'])
    st.metric("Reports Available", len(integrator.get_available_reports()))
```

### 2. Alert System
```python
def check_news_alerts():
    integrator = BankMuamalatDataIntegrator('latest_data.json')
    news = integrator.get_latest_news()
    
    # Check for important keywords
    alert_keywords = ['merger', 'akuisisi', 'restrukturisasi', 'peningkatan modal']
    
    for item in news:
        title = item.get('title', '').lower()
        if any(keyword in title for keyword in alert_keywords):
            send_alert(f"Important news: {item['title']}")
```

## 📞 Support & Maintenance

### 1. Regular Updates
```bash
# Update scraper monthly
git pull origin main
pip install -r requirements.txt --upgrade
```

### 2. Data Quality Checks
```python
def validate_scraped_data(data):
    checks = {
        'news_count': len(data.get('news', [])) > 0,
        'company_info': data.get('company_info', {}).get('data_found', False),
        'fresh_data': 'scrape_timestamp' in data
    }
    
    for check, passed in checks.items():
        print(f"{check}: {'✅' if passed else '❌'}")
```

### 3. Legal Compliance Review
```python
def compliance_check():
    # Check robots.txt compliance
    robots_ok = scraper.check_robots_txt()
    
    # Check rate limiting
    rate_ok = scraper.delay >= 2.0
    
    # Check data types
    data_ok = not_accessing_private_data()
    
    return all([robots_ok, rate_ok, data_ok])
```

## ⚠️ Legal & Ethical Guidelines

### DO's ✅
- ✅ Respect robots.txt
- ✅ Use reasonable delays (≥2 seconds)
- ✅ Only scrape public information
- ✅ Identify yourself with proper User-Agent
- ✅ Monitor and limit resource usage
- ✅ Check terms of service regularly
- ✅ Keep scraped data secure and private

### DON'Ts ❌
- ❌ Don't overload the server
- ❌ Don't scrape private/personal data
- ❌ Don't ignore robots.txt
- ❌ Don't scrape behind authentication
- ❌ Don't republish copyrighted content
- ❌ Don't use data for harmful purposes
- ❌ Don't scrape faster than 1 request/second

## 📞 Contact & Support

Untuk pertanyaan teknis atau legal:
- 📧 Email: your-email@company.com
- 📋 Issue Tracker: GitHub Issues
- 📖 Documentation: Wiki

**Remember: Selalu gunakan scraper dengan tanggung jawab dan sesuai dengan hukum yang berlaku!**