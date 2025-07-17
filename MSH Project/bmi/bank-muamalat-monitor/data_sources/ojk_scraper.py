import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import Dict, List, Optional
import logging
import time
import re

class OJKScraper:
    """Scraper untuk data OJK (Otoritas Jasa Keuangan)"""
    
    def __init__(self):
        self.base_url = "https://www.ojk.go.id"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.logger = logging.getLogger(__name__)
    
    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        """Ambil halaman web dan parse dengan BeautifulSoup"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            self.logger.error(f"Error fetching page {url}: {e}")
            return None
    
    def scrape_bank_data(self) -> List[Dict]:
        """Scrape data bank dari OJK"""
        bank_data = []
        try:
            url = f"{self.base_url}/id/kanal/perbankan/data-dan-statistik"
            soup = self.get_page(url)
            
            if soup:
                # Implementasi scraping sesuai struktur halaman OJK
                tables = soup.find_all('table')
                for table in tables:
                    rows = table.find_all('tr')
                    for row in rows[1:]:  # Skip header
                        cols = row.find_all('td')
                        if len(cols) >= 2:
                            bank_data.append({
                                'nama_bank': cols[0].get_text(strip=True),
                                'kode_bank': cols[1].get_text(strip=True) if len(cols) > 1 else '',
                                'status': cols[2].get_text(strip=True) if len(cols) > 2 else ''
                            })
        except Exception as e:
            self.logger.error(f"Error scraping bank data: {e}")
        
        return bank_data
    
    def scrape_statistics(self, category: str = "perbankan") -> Dict:
        """Scrape statistik dari OJK"""
        stats_data = {}
        try:
            url = f"{self.base_url}/id/kanal/{category}/data-dan-statistik"
            soup = self.get_page(url)
            
            if soup:
                # Ambil tabel statistik
                for table in soup.find_all('table'):
                    caption = table.find('caption')
                    if caption:
                        table_name = caption.get_text(strip=True)
                        table_data = []
                        
                        rows = table.find_all('tr')
                        headers = [th.get_text(strip=True) for th in rows[0].find_all(['th', 'td'])]
                        
                        for row in rows[1:]:
                            cols = row.find_all(['td', 'th'])
                            row_data = [col.get_text(strip=True) for col in cols]
                            if len(row_data) == len(headers):
                                table_data.append(dict(zip(headers, row_data)))
                        
                        stats_data[table_name] = table_data
        except Exception as e:
            self.logger.error(f"Error scraping statistics: {e}")
        
        return stats_data
    
    def scrape_regulations(self, page_limit: int = 5) -> List[Dict]:
        """Scrape peraturan terbaru dari OJK"""
        regulations = []
        try:
            for page in range(1, page_limit + 1):
                url = f"{self.base_url}/id/regulasi/peraturan-ojk?page={page}"
                soup = self.get_page(url)
                
                if soup:
                    items = soup.find_all('div', class_='regulation-item')
                    for item in items:
                        title_elem = item.find('h3') or item.find('h4')
                        date_elem = item.find('span', class_='date')
                        link_elem = item.find('a')
                        
                        regulation = {
                            'title': title_elem.get_text(strip=True) if title_elem else '',
                            'date': date_elem.get_text(strip=True) if date_elem else '',
                            'link': link_elem.get('href') if link_elem else ''
                        }
                        
                        if regulation['title']:
                            regulations.append(regulation)
                
                time.sleep(1)  # Rate limiting
        except Exception as e:
            self.logger.error(f"Error scraping regulations: {e}")
        
        return regulations
    
    def save_to_excel(self, data: Dict[str, List[Dict]], filename: str) -> bool:
        """Simpan data ke Excel"""
        try:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                for sheet_name, sheet_data in data.items():
                    if sheet_data:
                        df = pd.DataFrame(sheet_data)
                        df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
            return True
        except Exception as e:
            self.logger.error(f"Error saving to Excel: {e}")
            return False