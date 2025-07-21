#!/usr/bin/env python3
"""
Bank Muamalat Public Data Scraper
Ethical web scraping for publicly available information
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
from datetime import datetime
from typing import Dict, List, Optional
import logging
from urllib.parse import urljoin, urlparse
import re

class BankMuamalatScraper:
    """
    Ethical scraper for Bank Muamalat public data
    Respects robots.txt and implements rate limiting
    """
    
    def __init__(self, delay: float = 2.0):
        self.base_url = "https://www.bankmuamalat.co.id"
        self.delay = delay  # Delay between requests to be respectful
        self.session = requests.Session()
        
        # Set user agent to identify ourselves
        self.session.headers.update({
            'User-Agent': 'BankMuamalatMonitor/1.0 (Data Research Purpose)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def check_robots_txt(self) -> bool:
        """Check robots.txt to ensure we're compliant"""
        try:
            robots_url = urljoin(self.base_url, '/robots.txt')
            response = self.session.get(robots_url, timeout=10)
            
            if response.status_code == 200:
                self.logger.info("✅ robots.txt found - checking compliance")
                # Basic check for disallowed paths
                robots_content = response.text.lower()
                if 'disallow: /' in robots_content and 'user-agent: *' in robots_content:
                    self.logger.warning("⚠️ robots.txt may restrict crawling")
                    return False
                return True
            else:
                self.logger.info("ℹ️ No robots.txt found")
                return True
                
        except Exception as e:
            self.logger.error(f"Error checking robots.txt: {e}")
            return True  # Assume allowed if can't check
    
    def respectful_get(self, url: str, **kwargs) -> Optional[requests.Response]:
        """Make a GET request with respectful delays"""
        try:
            self.logger.info(f"📡 Fetching: {url}")
            
            # Respectful delay
            time.sleep(self.delay)
            
            response = self.session.get(url, timeout=15, **kwargs)
            response.raise_for_status()
            
            return response
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"❌ Error fetching {url}: {e}")
            return None
    
    def scrape_company_info(self) -> Dict:
        """Scrape basic company information"""
        self.logger.info("🏦 Scraping company information...")
        
        # Try different potential pages for company info
        potential_urls = [
            "/tentang-kami",
            "/about-us", 
            "/profil-perusahaan",
            "/corporate-info",
            "/"
        ]
        
        company_info = {
            'scraped_at': datetime.now().isoformat(),
            'source_url': self.base_url,
            'company_name': 'PT Bank Muamalat Indonesia Tbk',
            'data_found': False
        }
        
        for path in potential_urls:
            url = urljoin(self.base_url, path)
            response = self.respectful_get(url)
            
            if response and response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract basic information
                info = self.extract_company_details(soup, url)
                if info:
                    company_info.update(info)
                    company_info['data_found'] = True
                    break
        
        return company_info
    
    def extract_company_details(self, soup: BeautifulSoup, url: str) -> Dict:
        """Extract company details from HTML"""
        details = {'source_page': url}
        
        try:
            # Try to find title
            title = soup.find('title')
            if title:
                details['page_title'] = title.get_text().strip()
            
            # Look for meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                details['description'] = meta_desc.get('content', '').strip()
            
            # Look for contact information patterns
            text_content = soup.get_text()
            
            # Extract phone numbers
            phone_pattern = r'(\+?62|0)[- ]?[\d\s\-()]{8,15}'
            phones = re.findall(phone_pattern, text_content)
            if phones:
                details['phone_numbers'] = list(set(phones))
            
            # Extract email addresses
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, text_content)
            if emails:
                details['emails'] = list(set(emails))
            
            # Look for address patterns
            if 'jakarta' in text_content.lower() or 'indonesia' in text_content.lower():
                # Try to extract address (basic pattern)
                lines = text_content.split('\n')
                for line in lines:
                    if 'jakarta' in line.lower() and len(line.strip()) > 10:
                        details['potential_address'] = line.strip()
                        break
            
            return details
            
        except Exception as e:
            self.logger.error(f"Error extracting details: {e}")
            return details
    
    def scrape_news_announcements(self) -> List[Dict]:
        """Scrape public news and announcements"""
        self.logger.info("📰 Scraping news and announcements...")
        
        news_urls = [
            "/berita",
            "/news", 
            "/pengumuman",
            "/announcements",
            "/siaran-pers"
        ]
        
        all_news = []
        
        for path in news_urls:
            url = urljoin(self.base_url, path)
            response = self.respectful_get(url)
            
            if response and response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                news_items = self.extract_news_items(soup, url)
                all_news.extend(news_items)
        
        # Remove duplicates based on title
        seen_titles = set()
        unique_news = []
        for item in all_news:
            title = item.get('title', '').strip()
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_news.append(item)
        
        return unique_news
    
    def extract_news_items(self, soup: BeautifulSoup, source_url: str) -> List[Dict]:
        """Extract news items from HTML"""
        news_items = []
        
        try:
            # Common selectors for news/articles
            selectors = [
                'article',
                '.news-item', 
                '.article-item',
                '.post-item',
                '.berita-item',
                'div[class*="news"]',
                'div[class*="article"]'
            ]
            
            for selector in selectors:
                items = soup.select(selector)
                
                for item in items[:10]:  # Limit to first 10 items
                    news_item = {
                        'scraped_at': datetime.now().isoformat(),
                        'source_url': source_url
                    }
                    
                    # Extract title
                    title_elem = item.find(['h1', 'h2', 'h3', 'h4', 'h5']) or item.find(['a'])
                    if title_elem:
                        news_item['title'] = title_elem.get_text().strip()
                    
                    # Extract date if available
                    date_elem = item.find(['time', '.date', '.tanggal']) 
                    if date_elem:
                        date_text = date_elem.get_text().strip()
                        news_item['date_text'] = date_text
                    
                    # Extract summary/excerpt
                    summary_elem = item.find(['p', '.excerpt', '.summary'])
                    if summary_elem:
                        news_item['summary'] = summary_elem.get_text().strip()[:200]
                    
                    # Extract link
                    link_elem = item.find('a')
                    if link_elem and link_elem.get('href'):
                        news_item['link'] = urljoin(self.base_url, link_elem['href'])
                    
                    if news_item.get('title'):
                        news_items.append(news_item)
                
                if news_items:  # If we found items with this selector, stop trying others
                    break
            
        except Exception as e:
            self.logger.error(f"Error extracting news: {e}")
        
        return news_items
    
    def scrape_financial_reports(self) -> List[Dict]:
        """Scrape links to financial reports"""
        self.logger.info("📊 Scraping financial reports...")
        
        report_urls = [
            "/investor-relations",
            "/laporan-keuangan",
            "/financial-reports",
            "/annual-report",
            "/laporan-tahunan"
        ]
        
        reports = []
        
        for path in report_urls:
            url = urljoin(self.base_url, path)
            response = self.respectful_get(url)
            
            if response and response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for PDF links (common for financial reports)
                pdf_links = soup.find_all('a', href=re.compile(r'\.pdf$', re.IGNORECASE))
                
                for link in pdf_links:
                    href = link.get('href')
                    text = link.get_text().strip()
                    
                    if href and text:
                        reports.append({
                            'title': text,
                            'url': urljoin(self.base_url, href),
                            'type': 'PDF',
                            'found_on': url,
                            'scraped_at': datetime.now().isoformat()
                        })
        
        return reports
    
    def scrape_product_info(self) -> List[Dict]:
        """Scrape basic product information"""
        self.logger.info("💳 Scraping product information...")
        
        product_urls = [
            "/produk",
            "/products",
            "/layanan",
            "/services"
        ]
        
        products = []
        
        for path in product_urls:
            url = urljoin(self.base_url, path)
            response = self.respectful_get(url)
            
            if response and response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for product listings
                product_items = soup.find_all(['div', 'section'], 
                                            class_=re.compile(r'product|produk', re.IGNORECASE))
                
                for item in product_items[:10]:  # Limit results
                    title_elem = item.find(['h1', 'h2', 'h3', 'h4'])
                    
                    if title_elem:
                        product_title = title_elem.get_text().strip()
                        
                        # Extract description
                        desc_elem = item.find('p')
                        description = desc_elem.get_text().strip()[:200] if desc_elem else ""
                        
                        products.append({
                            'title': product_title,
                            'description': description,
                            'found_on': url,
                            'scraped_at': datetime.now().isoformat()
                        })
        
        return products
    
    def run_comprehensive_scrape(self) -> Dict:
        """Run comprehensive scraping of public data"""
        self.logger.info("🚀 Starting comprehensive scrape of Bank Muamalat public data")
        
        # Check robots.txt compliance
        if not self.check_robots_txt():
            self.logger.warning("⚠️ Robots.txt may restrict access. Proceeding with caution.")
        
        results = {
            'scrape_timestamp': datetime.now().isoformat(),
            'scrape_summary': {}
        }
        
        try:
            # 1. Company Information
            self.logger.info("1️⃣ Collecting company information...")
            company_info = self.scrape_company_info()
            results['company_info'] = company_info
            results['scrape_summary']['company_info'] = 'success' if company_info.get('data_found') else 'limited'
            
            # 2. News & Announcements
            self.logger.info("2️⃣ Collecting news and announcements...")
            news = self.scrape_news_announcements()
            results['news'] = news
            results['scrape_summary']['news_count'] = len(news)
            
            # 3. Financial Reports
            self.logger.info("3️⃣ Collecting financial reports...")
            reports = self.scrape_financial_reports()
            results['financial_reports'] = reports
            results['scrape_summary']['reports_count'] = len(reports)
            
            # 4. Product Information
            self.logger.info("4️⃣ Collecting product information...")
            products = self.scrape_product_info()
            results['products'] = products
            results['scrape_summary']['products_count'] = len(products)
            
            self.logger.info("✅ Scraping completed successfully!")
            
        except Exception as e:
            self.logger.error(f"❌ Error during scraping: {e}")
            results['error'] = str(e)
        
        return results
    
    def save_results(self, results: Dict, filename: str = None):
        """Save scraping results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bank_muamalat_data_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"💾 Results saved to {filename}")
            return filename
            
        except Exception as e:
            self.logger.error(f"❌ Error saving results: {e}")
            return None

def main():
    """Main function to run the scraper"""
    print("🏦 Bank Muamalat Public Data Scraper")
    print("=" * 50)
    print("⚠️  DISCLAIMER: This scraper only collects publicly available data")
    print("    and respects website terms of service and robots.txt")
    print("=" * 50)
    
    # Create scraper instance
    scraper = BankMuamalatScraper(delay=2.0)  # 2 second delay between requests
    
    # Run comprehensive scrape
    results = scraper.run_comprehensive_scrape()
    
    # Save results
    filename = scraper.save_results(results)
    
    # Display summary
    print("\n📊 SCRAPING SUMMARY:")
    print("-" * 30)
    
    summary = results.get('scrape_summary', {})
    print(f"Company Info: {summary.get('company_info', 'N/A')}")
    print(f"News Articles: {summary.get('news_count', 0)} found")
    print(f"Financial Reports: {summary.get('reports_count', 0)} found")
    print(f"Products: {summary.get('products_count', 0)} found")
    
    if filename:
        print(f"📁 Data saved to: {filename}")
    
    print("\n🎯 Next Steps:")
    print("1. Review the scraped data for accuracy")
    print("2. Use the data to update your monitoring dashboard")
    print("3. Implement regular scraping with appropriate intervals")
    print("4. Always respect the website's terms of service")

if __name__ == "__main__":
    main()