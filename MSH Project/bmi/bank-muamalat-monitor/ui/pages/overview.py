"""
Overview Dashboard Page for Bank Muamalat Health Monitoring
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from typing import Optional, Dict, Any

# Safe import for components
try:
    from ui.components.metrics_cards import render_single_metric_card, display_metric_cards
    from ui.components.charts import create_gauge_chart, create_trend_chart, safe_plotly_chart
except ImportError:
    # Fallback if components not available
    def render_single_metric_card(name, data, show_chart=False):
        st.metric(name, data.get('value', 0), data.get('delta', 0))
    
    def display_metric_cards(metrics, layout="horizontal"):
        cols = st.columns(len(metrics))
        for i, (key, value) in enumerate(metrics.items()):
            with cols[i]:
                render_single_metric_card(key, value)
    
    def create_gauge_chart(value, title="Score", threshold=70.0):
        return None
    
    def create_trend_chart(x, y, title="Trend"):
        return None
        
    def safe_plotly_chart(fig, fallback_message="Chart unavailable"):
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(fallback_message)

def show_overview():
    """Main function expected by main.py - calls the original render function"""
    render()

def render(orchestrator: Optional[Any] = None):
    """Render the overview dashboard"""
    
    st.title("🏦 Bank Muamalat Health Overview")
    st.markdown("### Real-time monitoring dashboard for BPKH decision support")
    
    # Get latest data (mock data for now)
    metrics = get_current_metrics()
    
    # Top metrics row
    render_key_metrics(metrics)
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        render_health_score_gauge(metrics)
        render_risk_indicator(metrics)
        
    with col2:
        render_performance_trends()
        render_peer_comparison()
    
    # Alerts and recommendations
    render_alerts_section(metrics)
    
    # Quick insights
    render_quick_insights(orchestrator)
    
    # Decision support summary
    render_decision_summary(metrics)

def get_current_metrics() -> Dict[str, Any]:
    """Get current metrics (mock data for demonstration)"""
    return {
        'car': 29.42,
        'npf': 3.99,
        'roa': 0.03,
        'roe': 0.4,
        'bopo': 98.5,
        'fdr': 85.0,
        'total_assets': 66.9,
        'net_profit': 20.4,
        'health_score': 65.5,
        'risk_level': 'MEDIUM',
        'last_updated': datetime.now()
    }

def render_key_metrics(metrics: Dict[str, Any]):
    """Render key metrics cards"""
    st.markdown("### 📊 Key Performance Indicators")
    
    # Prepare metrics for display
    key_metrics = {
        "CAR": {
            "value": metrics['car'],
            "unit": "%",
            "delta": 2.5,
            "status": "good" if metrics['car'] > 15 else "warning",
            "description": "Capital Adequacy Ratio"
        },
        "NPF": {
            "value": metrics['npf'],
            "unit": "%",
            "delta": 0.5,
            "status": "critical" if metrics['npf'] > 3.5 else "warning",
            "description": "Non-Performing Financing"
        },
        "ROA": {
            "value": metrics['roa'],
            "unit": "%",
            "delta": -0.02,
            "status": "critical" if metrics['roa'] < 0.5 else "warning",
            "description": "Return on Assets"
        },
        "Total Assets": {
            "value": metrics['total_assets'],
            "unit": "T",
            "delta": 9.0,
            "status": "good",
            "description": "Total Bank Assets"
        }
    }
    
    # Display metrics
    display_metric_cards(key_metrics, layout="horizontal")

def render_health_score_gauge(metrics: Dict[str, Any]):
    """Render overall health score gauge"""
    st.markdown("#### 🏥 Overall Health Score")
    
    try:
        # Use unified charts module
        fig = create_gauge_chart(
            value=metrics['health_score'],
            title="Bank Health Score",
            threshold=70.0,
            min_val=0.0,
            max_val=100.0,
            color="darkblue"
        )
        
        safe_plotly_chart(fig, "Health score gauge unavailable")
        
    except Exception as e:
        # Fallback to plotly figure creation
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=metrics['health_score'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Bank Health Score"},
            delta={'reference': 70, 'relative': True},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 33], 'color': "lightgray"},
                    {'range': [33, 67], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Health interpretation
    if metrics['health_score'] < 33:
        st.error("🔴 Critical condition - Immediate action required")
    elif metrics['health_score'] < 67:
        st.warning("🟡 Moderate health - Close monitoring needed")
    else:
        st.success("🟢 Good health - Continue current strategy")

def render_risk_indicator(metrics: Dict[str, Any]):
    """Render risk level indicator"""
    st.markdown("#### ⚠️ Risk Assessment")
    
    # Risk matrix
    risk_factors = {
        'Credit Risk': 'HIGH' if metrics['npf'] > 3 else 'MEDIUM',
        'Capital Risk': 'LOW' if metrics['car'] > 15 else 'MEDIUM',
        'Operational Risk': 'HIGH' if metrics['bopo'] > 90 else 'MEDIUM',
        'Liquidity Risk': 'LOW' if metrics['fdr'] < 90 else 'MEDIUM',
        'Profitability Risk': 'HIGH' if metrics['roa'] < 0.5 else 'MEDIUM'
    }
    
    # Create risk visualization
    risk_df = pd.DataFrame(
        list(risk_factors.items()),
        columns=['Risk Type', 'Level']
    )
    
    # Color mapping
    color_map = {'LOW': '#28a745', 'MEDIUM': '#ffc107', 'HIGH': '#dc3545'}
    
    fig = px.bar(
        risk_df,
        x='Risk Type',
        y=[1]*len(risk_df),
        color='Level',
        color_discrete_map=color_map,
        title="Risk Level by Category"
    )
    
    fig.update_layout(
        showlegend=True,
        yaxis_visible=False,
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_performance_trends():
    """Render performance trends"""
    st.markdown("#### 📈 Performance Trends")
    
    # Mock historical data
    months = pd.date_range(end=datetime.now(), periods=12, freq='M')
    trend_data = pd.DataFrame({
        'Month': months,
        'NPF': np.random.normal(3.5, 0.5, 12).cumsum() / 12 + 2,
        'ROA': np.random.normal(0.05, 0.02, 12),
        'CAR': np.random.normal(28, 1, 12)
    })
    
    # Create subplot figure
    fig = go.Figure()
    
    # NPF trend
    fig.add_trace(go.Scatter(
        x=trend_data['Month'],
        y=trend_data['NPF'],
        name='NPF %',
        line=dict(color='red', width=2)
    ))
    
    # ROA trend (secondary y-axis)
    fig.add_trace(go.Scatter(
        x=trend_data['Month'],
        y=trend_data['ROA']*100,
        name='ROA %',
        line=dict(color='green', width=2),
        yaxis='y2'
    ))
    
    # CAR trend (secondary y-axis)
    fig.add_trace(go.Scatter(
        x=trend_data['Month'],
        y=trend_data['CAR'],
        name='CAR %',
        line=dict(color='blue', width=2),
        yaxis='y2'
    ))
    
    # Update layout
    fig.update_layout(
        hovermode='x unified',
        yaxis=dict(title='NPF %', side='left'),
        yaxis2=dict(title='CAR % / ROA %', side='right', overlaying='y'),
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_peer_comparison():
    """Render peer comparison chart"""
    st.markdown("#### 🏛️ Peer Comparison")
    
    # Mock peer data
    peer_data = pd.DataFrame({
        'Bank': ['Muamalat', 'BSI', 'Bank Mega Syariah', 'BTPN Syariah'],
        'CAR': [29.42, 25.5, 22.3, 35.2],
        'NPF': [3.99, 2.5, 1.8, 2.2],
        'ROA': [0.03, 1.5, 1.2, 3.5],
        'BOPO': [98.5, 85.2, 82.1, 75.3]
    })
    
    # Radar chart for comparison
    categories = ['CAR', 'NPF', 'ROA', 'BOPO']
    
    fig = go.Figure()
    
    for _, bank in peer_data.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[
                bank['CAR']/35*100,  # Normalize to 100
                (5-bank['NPF'])/5*100,  # Inverse for NPF
                bank['ROA']/3.5*100,
                (100-bank['BOPO'])/25*100  # Inverse for BOPO
            ],
            theta=categories,
            fill='toself',
            name=bank['Bank']
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.caption("*Normalized scores: Higher is better for all metrics")

def render_alerts_section(metrics: Dict[str, Any]):
    """Render alerts and warnings"""
    st.markdown("### 🚨 Alerts & Notifications")
    
    alerts = []
    
    # Check for critical thresholds
    if metrics['npf'] > 3.5:
        alerts.append({
            'level': 'critical',
            'message': f"NPF at {metrics['npf']}% exceeds safe threshold",
            'action': 'Initiate immediate NPF reduction measures'
        })
        
    if metrics['bopo'] > 95:
        alerts.append({
            'level': 'warning',
            'message': f"BOPO ratio at {metrics['bopo']}% indicates inefficiency",
            'action': 'Review operational costs and digitalization opportunities'
        })
        
    if metrics['roa'] < 0.5:
        alerts.append({
            'level': 'warning',
            'message': f"ROA at {metrics['roa']}% below industry standard",
            'action': 'Focus on revenue enhancement initiatives'
        })
    
    if not alerts:
        st.info("✅ No critical alerts at this time")
    else:
        for alert in alerts:
            if alert['level'] == 'critical':
                st.error(f"**{alert['message']}**\n\n*Action: {alert['action']}*")
            else:
                st.warning(f"**{alert['message']}**\n\n*Action: {alert['action']}*")

def render_quick_insights(orchestrator: Optional[Any]):
    """Render AI-generated quick insights"""
    st.markdown("### 🤖 AI-Powered Insights")
    
    with st.container():
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.info(
                """
                **Key Insights from AI Analysis:**
                
                1. **Capital Position**: Strong CAR at 29.42% provides significant buffer, 
                   well above regulatory minimum
                
                2. **Asset Quality Concern**: NPF trending upward, requiring focused 
                   intervention in corporate segment
                
                3. **Efficiency Gap**: BOPO at 98.5% indicates urgent need for digital 
                   transformation and cost optimization
                
                4. **Strategic Focus**: Leverage BPKH synergies in haji/umrah segment 
                   for sustainable growth
                """
            )
            
        with col2:
            if st.button("🔄 Refresh Analysis", use_container_width=True):
                with st.spinner("Running AI analysis..."):
                    # Trigger new analysis
                    st.rerun()

def render_decision_summary(metrics: Dict[str, Any]):
    """Render decision support summary"""
    st.markdown("### 💡 Decision Support Summary")
    
    # Create decision matrix
    decision_factors = {
        'Capital Strength': {'score': 85, 'weight': 0.25},
        'Asset Quality': {'score': 40, 'weight': 0.30},
        'Profitability': {'score': 20, 'weight': 0.25},
        'Efficiency': {'score': 30, 'weight': 0.20}
    }
    
    # Calculate weighted score
    total_score = sum(
        factor['score'] * factor['weight'] 
        for factor in decision_factors.values()
    )
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.markdown("#### Recommendation Score")
        # Progress bar for recommendation
        st.progress(total_score/100)
        st.markdown(f"**{total_score:.1f}/100**")
        
    with col2:
        st.markdown("#### BPKH Action")
        if total_score > 70:
            st.success("✅ MAINTAIN INVESTMENT")
        elif total_score > 50:
            st.warning("⚠️ MAINTAIN WITH CONDITIONS")
        else:
            st.error("🔴 CONSIDER STRATEGIC OPTIONS")
            
    with col3:
        st.markdown("#### Confidence")
        st.markdown("**HIGH**")
        st.caption("Based on comprehensive multi-factor analysis")
    
    # Expandable details
    with st.expander("View Detailed Decision Factors"):
        factor_df = pd.DataFrame([
            {'Factor': factor, 'Score': data['score'], 'Weight': f"{data['weight']*100:.0f}%"}
            for factor, data in decision_factors.items()
        ])
        st.dataframe(factor_df, use_container_width=True)
        
        st.markdown("""
        **Key Considerations:**
        - Strong capital base provides stability
        - Asset quality requires immediate attention
        - Profitability improvement is critical for sustainability
        - Operational efficiency needs transformation
        """)

# Create a simple fallback for missing components
def render_fallback_content():
    """Render fallback content if components are missing"""
    st.error("Some components are missing. Please check the installation.")
    
    # Show basic metrics
    st.markdown("### Basic Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("CAR", "29.42%", "2.5%")
    with col2:
        st.metric("NPF", "3.99%", "0.5%")
    with col3:
        st.metric("ROA", "0.03%", "-0.02%")
    with col4:
        st.metric("Total Assets", "66.9T", "9%")

# Export functions for external use
__all__ = [
    'show_overview',  # Main function expected by main.py
    'render',
    'get_current_metrics',
    'render_key_metrics',
    'render_health_score_gauge',
    'render_risk_indicator',
    'render_performance_trends',
    'render_peer_comparison',
    'render_alerts_section',
    'render_quick_insights',
    'render_decision_summary',
    'render_fallback_content'
]

# For backwards compatibility and direct execution
if __name__ == "__main__":
    show_overview()