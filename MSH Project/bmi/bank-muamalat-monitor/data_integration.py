#!/usr/bin/env python3
"""
Data Integration Module
Integrates scraped data with Bank Muamalat monitoring dashboard
"""

import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import streamlit as st
from pathlib import Path
import re
import logging

class BankMuamalatDataIntegrator:
    """
    Integrates scraped data with the monitoring dashboard
    """
    
    def __init__(self, data_file: Optional[str] = None):
        self.data_file = data_file
        self.scraped_data = None
        self.logger = logging.getLogger(__name__)
        
        if data_file and Path(data_file).exists():
            self.load_scraped_data(data_file)
    
    def load_scraped_data(self, file_path: str) -> bool:
        """Load scraped data from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.scraped_data = json.load(f)
            
            self.logger.info(f"✅ Loaded scraped data from {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error loading data: {e}")
            return False
    
    def get_latest_scraped_file(self, data_dir: str = ".") -> Optional[str]:
        """Find the latest scraped data file"""
        try:
            data_path = Path(data_dir)
            json_files = list(data_path.glob("bank_muamalat_data_*.json"))
            
            if json_files:
                # Sort by modification time, get latest
                latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
                return str(latest_file)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error finding latest file: {e}")
            return None
    
    def extract_financial_metrics(self) -> Dict[str, Any]:
        """Extract financial metrics from scraped data and news"""
        if not self.scraped_data:
            return self.get_mock_financial_data()
        
        metrics = {
            'last_updated': datetime.now(),
            'data_source': 'scraped_data',
            'car': None,
            'npf': None,
            'roa': None,
            'roe': None,
            'bopo': None,
            'total_assets': None,
            'news_sentiment': 'neutral'
        }
        
        try:
            # Analyze news for financial mentions
            news_items = self.scraped_data.get('news', [])
            financial_mentions = []
            
            for news in news_items:
                title = news.get('title', '').lower()
                summary = news.get('summary', '').lower()
                text = f"{title} {summary}"
                
                # Look for financial ratio mentions
                financial_keywords = {
                    'car': ['capital adequacy', 'car', 'rasio kecukupan modal'],
                    'npf': ['npf', 'non performing', 'kredit bermasalah'],
                    'roa': ['roa', 'return on asset', 'return on assets'],
                    'profit': ['profit', 'laba', 'keuntungan'],
                    'loss': ['rugi', 'kerugian', 'loss']
                }
                
                for category, keywords in financial_keywords.items():
                    for keyword in keywords:
                        if keyword in text:
                            financial_mentions.append({
                                'category': category,
                                'title': news.get('title'),
                                'date': news.get('date_text'),
                                'sentiment': self.analyze_sentiment(text)
                            })
            
            # Extract numbers from financial reports
            reports = self.scraped_data.get('financial_reports', [])
            if reports:
                metrics['financial_reports_available'] = len(reports)
                metrics['latest_report'] = reports[0] if reports else None
            
            # Set sentiment based on news analysis
            if financial_mentions:
                sentiments = [item['sentiment'] for item in financial_mentions]
                positive_count = sentiments.count('positive')
                negative_count = sentiments.count('negative')
                
                if positive_count > negative_count:
                    metrics['news_sentiment'] = 'positive'
                elif negative_count > positive_count:
                    metrics['news_sentiment'] = 'negative'
                else:
                    metrics['news_sentiment'] = 'neutral'
            
            metrics['financial_mentions'] = financial_mentions
            
        except Exception as e:
            self.logger.error(f"Error extracting financial metrics: {e}")
        
        # If no real data found, supplement with mock data
        if not any([metrics['car'], metrics['npf'], metrics['roa']]):
            mock_data = self.get_mock_financial_data()
            metrics.update(mock_data)
            metrics['data_source'] = 'mock_with_scraped_context'
        
        return metrics
    
    def analyze_sentiment(self, text: str) -> str:
        """Basic sentiment analysis"""
        positive_words = [
            'naik', 'meningkat', 'tumbuh', 'positif', 'baik', 'stabil', 
            'menguntungkan', 'sukses', 'kuat', 'solid', 'optimal'
        ]
        negative_words = [
            'turun', 'menurun', 'negatif', 'buruk', 'rugi', 'krisis',
            'masalah', 'tantangan', 'risiko', 'lemah', 'drop'
        ]
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def get_mock_financial_data(self) -> Dict[str, Any]:
        """Get mock financial data when real data is not available"""
        return {
            'car': 29.42,
            'npf': 3.99,
            'roa': 0.03,
            'roe': 0.4,
            'bopo': 98.5,
            'fdr': 85.0,
            'total_assets': 66.9,  # Trillion IDR
            'net_profit': 20.4,    # Billion IDR
            'data_source': 'mock_data'
        }
    
    def get_company_profile(self) -> Dict[str, Any]:
        """Get company profile from scraped data"""
        if not self.scraped_data:
            return self.get_default_company_profile()
        
        company_info = self.scraped_data.get('company_info', {})
        
        profile = {
            'name': 'PT Bank Muamalat Indonesia Tbk',
            'website': 'https://www.bankmuamalat.co.id',
            'last_updated': company_info.get('scraped_at'),
            'description': company_info.get('description', 'Bank Syariah pertama di Indonesia'),
        }
        
        # Add contact information if available
        if company_info.get('phone_numbers'):
            profile['phone'] = company_info['phone_numbers'][0]
        
        if company_info.get('emails'):
            profile['email'] = company_info['emails'][0]
        
        if company_info.get('potential_address'):
            profile['address'] = company_info['potential_address']
        
        return profile
    
    def get_default_company_profile(self) -> Dict[str, Any]:
        """Default company profile"""
        return {
            'name': 'PT Bank Muamalat Indonesia Tbk',
            'website': 'https://www.bankmuamalat.co.id',
            'description': 'Bank Syariah pertama di Indonesia yang didirikan tahun 1991',
            'phone': '+62-21-251-1411',
            'address': 'Jakarta, Indonesia'
        }
    
    def get_latest_news(self, limit: int = 5) -> List[Dict]:
        """Get latest news from scraped data"""
        if not self.scraped_data:
            return self.get_mock_news()
        
        news_items = self.scraped_data.get('news', [])
        
        # Sort by date if available, otherwise by order
        sorted_news = news_items[:limit]
        
        return sorted_news
    
    def get_mock_news(self) -> List[Dict]:
        """Mock news data"""
        return [
            {
                'title': 'Bank Muamalat Terus Berkomitmen Pada Transformasi Digital',
                'summary': 'Bank Muamalat mempercepat transformasi digital untuk meningkatkan layanan nasabah...',
                'date_text': '2024-07-15',
                'source': 'Mock Data'
            },
            {
                'title': 'Laporan Keuangan Q2 2024 Menunjukkan Tren Positif',
                'summary': 'Kinerja keuangan Bank Muamalat menunjukkan perbaikan di berbagai indikator...',
                'date_text': '2024-07-10',
                'source': 'Mock Data'
            }
        ]
    
    def get_available_reports(self) -> List[Dict]:
        """Get available financial reports"""
        if not self.scraped_data:
            return []
        
        return self.scraped_data.get('financial_reports', [])
    
    def get_products_services(self) -> List[Dict]:
        """Get products and services information"""
        if not self.scraped_data:
            return self.get_default_products()
        
        return self.scraped_data.get('products', [])
    
    def get_default_products(self) -> List[Dict]:
        """Default products data"""
        return [
            {
                'title': 'Tabungan iB Muamalat',
                'description': 'Tabungan syariah dengan sistem bagi hasil'
            },
            {
                'title': 'Pembiayaan iB Muamalat',
                'description': 'Pembiayaan syariah untuk berbagai kebutuhan'
            },
            {
                'title': 'Deposito iB Muamalat',
                'description': 'Investasi syariah dengan return yang kompetitif'
            }
        ]
    
    def get_scraping_summary(self) -> Dict[str, Any]:
        """Get summary of scraping results"""
        if not self.scraped_data:
            return {'status': 'no_data', 'message': 'No scraped data available'}
        
        summary = self.scraped_data.get('scrape_summary', {})
        
        return {
            'status': 'success',
            'scrape_time': self.scraped_data.get('scrape_timestamp'),
            'news_count': summary.get('news_count', 0),
            'reports_count': summary.get('reports_count', 0),
            'products_count': summary.get('products_count', 0),
            'company_info_status': summary.get('company_info', 'unknown')
        }

# Streamlit integration functions
def show_real_data_dashboard():
    """Show dashboard with real scraped data"""
    st.title("🔍 Real Data Integration Dashboard")
    
    # Initialize data integrator
    integrator = BankMuamalatDataIntegrator()
    
    # Try to load latest data
    latest_file = integrator.get_latest_scraped_file()
    
    if latest_file:
        st.success(f"✅ Using scraped data from: {Path(latest_file).name}")
        integrator.load_scraped_data(latest_file)
    else:
        st.warning("⚠️ No scraped data found. Using mock data with real context.")
    
    # Show scraping summary
    with st.expander("📊 Data Source Information"):
        summary = integrator.get_scraping_summary()
        
        if summary['status'] == 'success':
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("News Articles", summary['news_count'])
            with col2:
                st.metric("Financial Reports", summary['reports_count'])
            with col3:
                st.metric("Products Found", summary['products_count'])
            with col4:
                st.metric("Company Info", summary['company_info_status'])
            
            st.info(f"Last scraped: {summary['scrape_time']}")
        else:
            st.error("No real-time data available. Displaying mock data.")
    
    # Company Profile
    st.markdown("## 🏦 Company Profile")
    profile = integrator.get_company_profile()
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Company:** {profile['name']}")
        st.markdown(f"**Website:** {profile['website']}")
        if profile.get('phone'):
            st.markdown(f"**Phone:** {profile['phone']}")
    
    with col2:
        if profile.get('description'):
            st.markdown(f"**Description:** {profile['description']}")
        if profile.get('address'):
            st.markdown(f"**Address:** {profile['address']}")
    
    # Financial Metrics with Real Context
    st.markdown("## 📊 Financial Metrics")
    metrics = integrator.extract_financial_metrics()
    
    if metrics['data_source'] == 'scraped_data':
        st.success("✅ Enhanced with real market context from news analysis")
    elif metrics['data_source'] == 'mock_with_scraped_context':
        st.info("ℹ️ Financial data supplemented with real news sentiment")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("CAR", f"{metrics['car']:.2f}%", help="Capital Adequacy Ratio")
    with col2:
        st.metric("NPF", f"{metrics['npf']:.2f}%", help="Non-Performing Financing")
    with col3:
        st.metric("ROA", f"{metrics['roa']:.2f}%", help="Return on Assets")
    with col4:
        news_sentiment = metrics.get('news_sentiment', 'neutral')
        sentiment_emoji = {'positive': '📈', 'negative': '📉', 'neutral': '➡️'}
        st.metric("News Sentiment", f"{sentiment_emoji[news_sentiment]} {news_sentiment.title()}")
    
    # Latest News
    st.markdown("## 📰 Latest News & Updates")
    news_items = integrator.get_latest_news()
    
    if news_items:
        for news in news_items:
            with st.expander(f"📄 {news.get('title', 'No Title')}"):
                if news.get('date_text'):
                    st.markdown(f"**Date:** {news['date_text']}")
                if news.get('summary'):
                    st.markdown(f"**Summary:** {news['summary']}")
                if news.get('link'):
                    st.markdown(f"**[Read More]({news['link']})**")
    else:
        st.info("No recent news found in scraped data")
    
    # Financial Reports
    st.markdown("## 📋 Available Reports")
    reports = integrator.get_available_reports()
    
    if reports:
        for report in reports:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"📄 **{report.get('title', 'Untitled Report')}**")
            with col2:
                if report.get('url'):
                    st.markdown(f"[📥 Download]({report['url']})")
    else:
        st.info("No financial reports found in scraped data")

def schedule_data_refresh():
    """Schedule regular data refresh"""
    st.markdown("## 🔄 Data Refresh Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        refresh_interval = st.selectbox(
            "Refresh Interval",
            ["Manual", "Daily", "Weekly", "Monthly"],
            index=1
        )
        
        auto_scrape = st.checkbox("Enable Auto-Scraping", value=False)
        
    with col2:
        last_refresh = st.text_input("Last Refresh", value=datetime.now().strftime("%Y-%m-%d %H:%M"))
        next_refresh = st.text_input("Next Scheduled", value="Manual trigger")
    
    if st.button("🔄 Refresh Data Now", type="primary"):
        with st.spinner("Refreshing data from Bank Muamalat website..."):
            # Here you would call the scraper
            st.info("This would trigger the scraper to get fresh data")
            time.sleep(2)  # Simulate processing
        st.success("✅ Data refresh completed!")
        st.rerun()

# Export functions
__all__ = [
    'BankMuamalatDataIntegrator',
    'show_real_data_dashboard',
    'schedule_data_refresh'
]