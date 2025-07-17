"""
Financial Health Page for Bank Muamalat Health Monitoring
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
from typing import Optional, Any

def render(orchestrator: Optional[Any] = None):
    """Render the financial health page"""
    
    st.title("💰 Financial Health Analysis")
    st.markdown("### Comprehensive financial performance monitoring")
    
    # Financial metrics overview
    render_financial_metrics()
    
    # Profitability analysis
    render_profitability_analysis()
    
    # Asset quality analysis
    render_asset_quality()
    
    # Efficiency metrics
    render_efficiency_metrics()

def render_financial_metrics():
    """Render key financial metrics"""
    st.markdown("## 📊 Key Financial Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Assets", "Rp 66.9T", "9% YoY")
    with col2:
        st.metric("Net Profit", "Rp 20.4B", "5% YoY")
    with col3:
        st.metric("ROA", "0.03%", "-0.02%")
    with col4:
        st.metric("ROE", "0.4%", "-0.1%")

def render_profitability_analysis():
    """Render profitability analysis"""
    st.markdown("## 📈 Profitability Analysis")
    
    # Mock data for profitability trends
    months = pd.date_range(end=datetime.now(), periods=12, freq='ME')
    profit_data = pd.DataFrame({
        'Month': months,
        'Net Profit': [15, 16, 18, 20, 22, 19, 21, 23, 20, 18, 19, 20.4],
        'ROA': [0.05, 0.04, 0.06, 0.07, 0.08, 0.06, 0.07, 0.08, 0.06, 0.04, 0.05, 0.03],
        'ROE': [0.6, 0.5, 0.7, 0.8, 0.9, 0.7, 0.8, 0.9, 0.7, 0.5, 0.6, 0.4]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=profit_data['Month'], y=profit_data['Net Profit'], name='Net Profit (B)'))
    fig.add_trace(go.Scatter(x=profit_data['Month'], y=profit_data['ROA'], name='ROA (%)', yaxis='y2'))
    fig.add_trace(go.Scatter(x=profit_data['Month'], y=profit_data['ROE'], name='ROE (%)', yaxis='y2'))
    
    fig.update_layout(
        title="Profitability Trends",
        xaxis_title="Month",
        yaxis_title="Net Profit (Billion IDR)",
        yaxis2=dict(title="Ratio (%)", overlaying='y', side='right'),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_asset_quality():
    """Render asset quality metrics"""
    st.markdown("## 🏛️ Asset Quality")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("NPF Gross", "3.99%", "0.5%")
        st.metric("NPF Net", "1.8%", "0.2%")
        st.metric("PPAP Coverage", "125.5%", "5.2%")
    
    with col2:
        # NPF breakdown
        npf_data = pd.DataFrame({
            'Category': ['Performing', 'Special Mention', 'Substandard', 'Doubtful', 'Loss'],
            'Percentage': [89.2, 7.6, 2.1, 0.8, 0.3]
        })
        
        fig = px.pie(npf_data, values='Percentage', names='Category', title='Financing Portfolio Quality')
        st.plotly_chart(fig, use_container_width=True)

def render_efficiency_metrics():
    """Render efficiency metrics"""
    st.markdown("## ⚡ Efficiency Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("BOPO", "98.5%", "2.1%")
        st.metric("NIM", "4.25%", "0.08%")
    
    with col2:
        # BOPO comparison
        bopo_data = pd.DataFrame({
            'Bank': ['Muamalat', 'BSI', 'Bank Mega Syariah', 'Industry Avg'],
            'BOPO': [98.5, 85.2, 82.1, 88.0]
        })
        
        fig = px.bar(bopo_data, x='Bank', y='BOPO', title='BOPO Comparison')
        fig.add_hline(y=90, line_dash="dash", annotation_text="Target")
        st.plotly_chart(fig, use_container_width=True)

# Export the render function
__all__ = ['render']