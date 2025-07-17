"""
Main dashboard interface for Bank Muamalat Health Monitor
"""

import streamlit as st
from typing import Dict, Any, Optional
import pandas as pd
from datetime import datetime

from ui.components.metrics_cards import display_metric_cards
from ui.components.charts import create_performance_chart, create_comparison_chart
from ui.components.risk_matrix import display_risk_matrix
from app.utils.helpers import format_currency, format_percentage, get_risk_color

class Dashboard:
    """
    Main dashboard class for Bank Muamalat monitoring
    """
    
    def __init__(self, config):
        self.config = config
        self.initialize_layout()
        
    def initialize_layout(self):
        """Initialize dashboard layout"""
        st.set_page_config(
            page_title="Bank Muamalat Dashboard",
            page_icon="🏦",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS
        st.markdown("""
        <style>
        .dashboard-header {
            background: linear-gradient(135deg, #4B0082 0%, #8A2BE2 100%);
            padding: 2rem;
            border-radius: 10px;
            color: white;
            margin-bottom: 2rem;
        }
        .metric-container {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        .metric-container:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        .alert-banner {
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
            font-weight: 500;
        }
        .alert-critical {
            background-color: #f8d7da;
            color: #721c24;
            border-left: 5px solid #dc3545;
        }
        .alert-warning {
            background-color: #fff3cd;
            color: #856404;
            border-left: 5px solid #ffc107;
        }
        .alert-success {
            background-color: #d4edda;
            color: #155724;
            border-left: 5px solid #28a745;
        }
        </style>
        """, unsafe_allow_html=True)
        
    def render(self, data: Optional[Dict[str, Any]] = None):
        """Render the main dashboard"""
        # Header
        self.render_header()
        
        # Key Metrics
        self.render_key_metrics(data)
        
        # Alerts
        self.render_alerts(data)
        
        # Main content area
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self.render_performance_charts(data)
            self.render_trend_analysis(data)
            
        with col2:
            self.render_risk_dashboard(data)
            self.render_quick_insights(data)
            
        # Footer
        self.render_footer()
        
    def render_header(self):
        """Render dashboard header"""
        st.markdown("""
        <div class="dashboard-header">
            <h1 style='margin: 0;'>🏦 Bank Muamalat Health Monitor</h1>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>
                Real-time Monitoring Dashboard for BPKH Decision Support
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Last update time
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.info(f"📅 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        with col2:
            if st.button("🔄 Refresh Data"):
                st.rerun()
        with col3:
            if st.button("📊 Generate Report"):
                st.info("Report generation started...")
                
    def render_key_metrics(self, data: Optional[Dict[str, Any]]):
        """Render key performance metrics"""
        st.markdown("### 📊 Key Performance Indicators")
        
        # Mock data if not provided
        if not data:
            data = self.get_mock_data()
            
        metrics = data.get('metrics', {})
        
        # Create metric columns
        cols = st.columns(6)
        
        # CAR
        with cols[0]:
            car_value = metrics.get('car', 29.42)
            car_delta = metrics.get('car_delta', 2.5)
            self.render_metric_card(
                "CAR",
                f"{car_value}%",
                f"{car_delta}%",
                "green" if car_value > 15 else "red",
                "Capital Adequacy Ratio"
            )
            
        # NPF
        with cols[1]:
            npf_value = metrics.get('npf', 3.99)
            npf_delta = metrics.get('npf_delta', 0.5)
            self.render_metric_card(
                "NPF",
                f"{npf_value}%",
                f"+{npf_delta}%",
                "red" if npf_value > 3 else "green",
                "Non-Performing Financing"
            )
            
        # ROA
        with cols[2]:
            roa_value = metrics.get('roa', 0.03)
            self.render_metric_card(
                "ROA",
                f"{roa_value}%",
                "-0.02%",
                "red" if roa_value < 1 else "green",
                "Return on Assets"
            )
            
        # ROE
        with cols[3]:
            roe_value = metrics.get('roe', 0.4)
            self.render_metric_card(
                "ROE",
                f"{roe_value}%",
                "-0.1%",
                "red" if roe_value < 10 else "green",
                "Return on Equity"
            )
            
        # BOPO
        with cols[4]:
            bopo_value = metrics.get('bopo', 98.5)
            self.render_metric_card(
                "BOPO",
                f"{bopo_value}%",
                "+1.2%",
                "red" if bopo_value > 90 else "green",
                "Operating Efficiency"
            )
            
        # FDR
        with cols[5]:
            fdr_value = metrics.get('fdr', 85.0)
            self.render_metric_card(
                "FDR",
                f"{fdr_value}%",
                "-2.3%",
                "green" if 80 <= fdr_value <= 90 else "yellow",
                "Financing to Deposit"
            )
            
    def render_metric_card(self, label: str, value: str, delta: str, status: str, tooltip: str):
        """Render individual metric card"""
        color_map = {
            'green': '#28a745',
            'yellow': '#ffc107',
            'red': '#dc3545'
        }
        
        st.markdown(f"""
        <div class="metric-container" style="border-top: 3px solid {color_map.get(status, '#6c757d')};">
            <h4 style="margin: 0; color: #666;">{label}</h4>
            <h2 style="margin: 0.5rem 0; color: {color_map.get(status, '#333')};">{value}</h2>
            <p style="margin: 0; font-size: 0.9rem; color: #999;">
                {delta} vs last period
            </p>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; color: #666;">
                {tooltip}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    def render_alerts(self, data: Optional[Dict[str, Any]]):
        """Render alert messages"""
        st.markdown("### 🚨 Alerts & Notifications")
        
        alerts = data.get('alerts', []) if data else self.get_mock_alerts()
        
        if not alerts:
            st.success("✅ No critical alerts at this time")
        else:
            for alert in alerts:
                alert_class = f"alert-{alert['level']}"
                st.markdown(f"""
                <div class="alert-banner {alert_class}">
                    <strong>{alert['title']}</strong><br>
                    {alert['message']}
                </div>
                """, unsafe_allow_html=True)
                
    def render_performance_charts(self, data: Optional[Dict[str, Any]]):
        """Render performance charts"""
        st.markdown("### 📈 Performance Trends")
        
        # Create tabs for different chart views
        tab1, tab2, tab3 = st.tabs(["Financial Metrics", "Asset Quality", "Efficiency"])
        
        with tab1:
            # Financial metrics trend chart
            chart_data = self.prepare_financial_chart_data(data)
            st.plotly_chart(
                create_performance_chart(chart_data, "Financial Performance Trends"),
                use_container_width=True
            )
            
        with tab2:
            # Asset quality charts
            npf_data = self.prepare_npf_chart_data(data)
            st.plotly_chart(
                create_performance_chart(npf_data, "NPF Trend Analysis"),
                use_container_width=True
            )
            
        with tab3:
            # Efficiency metrics
            efficiency_data = self.prepare_efficiency_chart_data(data)
            st.plotly_chart(
                create_performance_chart(efficiency_data, "Operational Efficiency"),
                use_container_width=True
            )
            
    def render_risk_dashboard(self, data: Optional[Dict[str, Any]]):
        """Render risk assessment dashboard"""
        st.markdown("### ⚠️ Risk Assessment")
        
        risk_data = data.get('risk_matrix', {}) if data else self.get_mock_risk_data()
        
        # Display risk matrix
        display_risk_matrix(risk_data)
        
        # Risk score summary
        st.markdown("#### Overall Risk Score")
        risk_score = risk_data.get('overall_score', 65)
        risk_level = risk_data.get('risk_level', 'MEDIUM')
        
        # Progress bar for risk score
        progress_color = get_risk_color(risk_level)
        st.markdown(f"""
        <div style="background: #f0f0f0; border-radius: 10px; padding: 1rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>Risk Score</span>
                <span style="font-weight: bold; color: {progress_color};">{risk_score}/100</span>
            </div>
            <div style="background: #ddd; border-radius: 5px; height: 20px; overflow: hidden;">
                <div style="background: {progress_color}; width: {risk_score}%; height: 100%;"></div>
            </div>
            <p style="text-align: center; margin-top: 0.5rem; color: {progress_color}; font-weight: bold;">
                {risk_level} RISK
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    def render_trend_analysis(self, data: Optional[Dict[str, Any]]):
        """Render trend analysis section"""
        st.markdown("### 📊 Comparative Analysis")
        
        # Peer comparison
        comparison_data = self.prepare_peer_comparison_data(data)
        st.plotly_chart(
            create_comparison_chart(comparison_data, "Peer Bank Comparison"),
            use_container_width=True
        )
        
    def render_quick_insights(self, data: Optional[Dict[str, Any]]):
        """Render AI-generated insights"""
        st.markdown("### 💡 Quick Insights")
        
        insights = data.get('insights', []) if data else self.get_mock_insights()
        
        for insight in insights:
            with st.expander(f"{insight['icon']} {insight['title']}", expanded=True):
                st.write(insight['content'])
                if insight.get('recommendation'):
                    st.info(f"💡 **Recommendation:** {insight['recommendation']}")
                    
    def render_footer(self):
        """Render dashboard footer"""
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666; font-size: 0.9rem;'>
            <p>© 2024 BPKH - Bank Muamalat Health Monitoring System</p>
            <p>Powered by RAG & Agentic AI | McKinsey & PwC Consulting</p>
        </div>
        """, unsafe_allow_html=True)
        
    # Data preparation methods
    def get_mock_data(self) -> Dict[str, Any]:
        """Get mock data for testing"""
        return {
            'metrics': {
                'car': 29.42,
                'car_delta': 2.5,
                'npf': 3.99,
                'npf_delta': 0.5,
                'roa': 0.03,
                'roe': 0.4,
                'bopo': 98.5,
                'fdr': 85.0
            },
            'timestamp': datetime.now().isoformat()
        }
        
    def get_mock_alerts(self) -> list:
        """Get mock alerts"""
        return [
            {
                'level': 'critical',
                'title': 'NPF Approaching Critical Threshold',
                'message': 'Non-Performing Financing at 3.99% is approaching the 5% regulatory limit. Immediate action required.'
            },
            {
                'level': 'warning',
                'title': 'Operational Efficiency Concern',
                'message': 'BOPO ratio at 98.5% indicates significant operational inefficiencies. Cost optimization needed.'
            }
        ]
        
    def get_mock_risk_data(self) -> Dict[str, Any]:
        """Get mock risk data"""
        return {
            'overall_score': 65,
            'risk_level': 'MEDIUM',
            'categories': {
                'Credit Risk': 75,
                'Operational Risk': 70,
                'Market Risk': 45,
                'Liquidity Risk': 30,
                'Compliance Risk': 50
            }
        }
        
    def get_mock_insights(self) -> list:
        """Get mock insights"""
        return [
            {
                'icon': '📈',
                'title': 'Capital Position Strong',
                'content': 'CAR at 29.42% provides significant buffer above regulatory minimum of 8%. This is a key strength that can support growth initiatives.',
                'recommendation': 'Leverage strong capital position for strategic expansion in profitable segments.'
            },
            {
                'icon': '⚠️',
                'title': 'Asset Quality Deteriorating',
                'content': 'NPF trending upward from 3.5% to 3.99% over the last quarter. Corporate segment showing particular stress.',
                'recommendation': 'Implement targeted NPF reduction program with focus on corporate recovery.'
            },
            {
                'icon': '💰',
                'title': 'Efficiency Gap',
                'content': 'BOPO at 98.5% is significantly above industry best practice of 80-85%. Digital transformation can help reduce costs.',
                'recommendation': 'Accelerate digital initiatives and branch optimization to improve efficiency.'
            }
        ]
        
    def prepare_financial_chart_data(self, data: Optional[Dict[str, Any]]) -> pd.DataFrame:
        """Prepare data for financial charts"""
        # Mock time series data
        dates = pd.date_range(end=datetime.now(), periods=12, freq='M')
        return pd.DataFrame({
            'Date': dates,
            'CAR': [27.5, 27.8, 28.1, 28.5, 28.3, 28.7, 29.0, 29.2, 29.1, 29.3, 29.4, 29.42],
            'ROA': [0.08, 0.07, 0.06, 0.05, 0.05, 0.04, 0.04, 0.03, 0.03, 0.03, 0.03, 0.03],
            'ROE': [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.5, 0.4, 0.4, 0.4, 0.4, 0.4]
        })
        
    def prepare_npf_chart_data(self, data: Optional[Dict[str, Any]]) -> pd.DataFrame:
        """Prepare NPF trend data"""
        dates = pd.date_range(end=datetime.now(), periods=12, freq='M')
        return pd.DataFrame({
            'Date': dates,
            'NPF Gross': [3.2, 3.3, 3.4, 3.5, 3.6, 3.6, 3.7, 3.8, 3.8, 3.9, 3.95, 3.99],
            'NPF Net': [2.1, 2.2, 2.3, 2.3, 2.4, 2.4, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5],
            'Industry Avg': [2.5, 2.5, 2.6, 2.6, 2.7, 2.7, 2.8, 2.8, 2.9, 2.9, 3.0, 3.0]
        })
        
    def prepare_efficiency_chart_data(self, data: Optional[Dict[str, Any]]) -> pd.DataFrame:
        """Prepare efficiency metrics data"""
        dates = pd.date_range(end=datetime.now(), periods=12, freq='M')
        return pd.DataFrame({
            'Date': dates,
            'BOPO': [95.2, 95.5, 95.8, 96.1, 96.5, 96.8, 97.2, 97.5, 97.8, 98.1, 98.3, 98.5],
            'CIR': [88.5, 88.8, 89.1, 89.5, 89.8, 90.2, 90.5, 90.8, 91.2, 91.5, 91.8, 92.1]
        })
        
    def prepare_peer_comparison_data(self, data: Optional[Dict[str, Any]]) -> pd.DataFrame:
        """Prepare peer comparison data"""
        return pd.DataFrame({
            'Bank': ['Muamalat', 'BSI', 'Bank Mega Syariah', 'BTPN Syariah', 'Industry Avg'],
            'CAR': [29.42, 25.5, 22.3, 35.2, 24.8],
            'NPF': [3.99, 2.5, 1.8, 2.2, 2.7],
            'ROA': [0.03, 1.5, 1.2, 3.5, 1.8],
            'BOPO': [98.5, 85.2, 82.1, 75.3, 83.5]
        })

# Standalone render function for direct use
def render_dashboard(config, data: Optional[Dict[str, Any]] = None):
    """Render dashboard with given configuration and data"""
    dashboard = Dashboard(config)
    dashboard.render(data)