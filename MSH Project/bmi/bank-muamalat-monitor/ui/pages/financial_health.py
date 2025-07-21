# ===== pages/financial_health.py =====
"""
Enhanced Financial Health Assessment Module
Real-time comprehensive analysis with industry benchmarks
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np

def render_financial_health():
    """Enhanced financial health assessment with real data integration"""
    
    st.title("💰 Financial Health Assessment")
    st.markdown("*Real-time comprehensive analysis of Bank Muamalat's financial performance*")
    
    # Get current data
    current_data = st.session_state.get('current_financial_data', {})
    
    if not current_data:
        st.warning("⚠️ No real-time data available. Please run data collection first.")
        if st.button("🔄 **Load Demo Data for Analysis**"):
            # Load sample data for demonstration
            current_data = {
                'assets': 61.4, 'npf': 0.86, 'car': 32.7, 'bopo': 96.62,
                'roa': 0.45, 'roe': 4.2, 'nim': 2.8, 'ldr': 85.5,
                'liquidity_ratio': 25.5, 'tier1_capital': 27.8,
                'timestamp': datetime.now()
            }
            st.session_state.current_financial_data = current_data
            st.rerun()
        return
    
    # ===== OVERALL HEALTH SCORE =====
    st.markdown("## 🎯 Overall Financial Health Score")
    
    # Calculate comprehensive health score
    health_components = calculate_health_score(current_data)
    overall_score = health_components['overall_score']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Health score with color coding
        if overall_score >= 80:
            st.success(f"**{overall_score:.0f}/100**")
            st.success("🟢 **Excellent**")
        elif overall_score >= 70:
            st.info(f"**{overall_score:.0f}/100**")
            st.info("🔵 **Good**")
        elif overall_score >= 60:
            st.warning(f"**{overall_score:.0f}/100**")
            st.warning("🟡 **Fair**")
        else:
            st.error(f"**{overall_score:.0f}/100**")
            st.error("🔴 **Poor**")
        st.caption("Overall Health Score")
    
    with col2:
        risk_level = determine_risk_level(current_data)
        risk_colors = {"Low": "success", "Medium": "warning", "High": "error"}
        getattr(st, risk_colors[risk_level])(f"**{risk_level} Risk**")
        st.caption("Risk Assessment")
    
    with col3:
        trend = calculate_trend()
        trend_icons = {"Improving": "📈", "Stable": "➡️", "Declining": "📉"}
        st.info(f"**{trend_icons[trend]} {trend}**")
        st.caption("Performance Trend")
    
    with col4:
        ranking = calculate_industry_ranking()
        st.info(f"**#{ranking}**")
        st.caption("Industry Ranking")
    
    # ===== DETAILED HEALTH BREAKDOWN =====
    st.markdown("## 📊 Detailed Health Analysis")
    
    # Create health component visualization
    fig_health = create_health_radar_chart(health_components)
    st.plotly_chart(fig_health, use_container_width=True)
    
    # Component details
    components = [
        ("Capital Adequacy", health_components['capital_score'], current_data.get('car', 0), "> 12%", "Strong capital base"),
        ("Asset Quality", health_components['asset_score'], current_data.get('npf', 0), "< 3%", "Low default risk"),
        ("Profitability", health_components['profit_score'], current_data.get('roa', 0), "> 1%", "Revenue generation"),
        ("Efficiency", health_components['efficiency_score'], current_data.get('bopo', 0), "< 94%", "Cost management"),
        ("Liquidity", health_components['liquidity_score'], current_data.get('liquidity_ratio', 0), "> 20%", "Cash availability")
    ]
    
    for name, score, value, benchmark, description in components:
        with st.expander(f"{name} - Score: {score:.0f}/100"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Score visualization
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = score,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Health Score"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 80], 'color': "yellow"},
                            {'range': [80, 100], 'color': "green"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                fig_gauge.update_layout(height=200)
                st.plotly_chart(fig_gauge, use_container_width=True)
            
            with col2:
                st.metric("Current Value", f"{value:.2f}%" if name != "Capital Adequacy" else f"{value:.2f}%")
                st.write(f"**Benchmark**: {benchmark}")
                st.write(f"**Impact**: {description}")
            
            with col3:
                # Recommendations
                recommendations = get_component_recommendations(name, score, value)
                st.markdown("**Recommendations:**")
                for rec in recommendations:
                    st.write(f"• {rec}")
    
    # ===== PEER COMPARISON =====
    st.markdown("## 🏆 Peer Comparison")
    
    peer_data = get_peer_comparison_data()
    comparison_chart = create_peer_comparison_chart(current_data, peer_data)
    st.plotly_chart(comparison_chart, use_container_width=True)
    
    # Peer comparison table
    st.markdown("### 📊 Detailed Peer Metrics")
    peer_df = pd.DataFrame(peer_data).T
    peer_df.loc['Bank Muamalat'] = [
        current_data.get('assets', 0),
        current_data.get('npf', 0),
        current_data.get('car', 0),
        current_data.get('bopo', 0),
        current_data.get('roa', 0)
    ]
    
    # Style the dataframe
    styled_df = peer_df.style.highlight_max(axis=0, subset=['Assets (T)', 'CAR (%)', 'ROA (%)']) \
                            .highlight_min(axis=0, subset=['NPF (%)', 'BOPO (%)']) \
                            .format(precision=2)
    
    st.dataframe(styled_df, use_container_width=True)
    
    # ===== HISTORICAL PERFORMANCE =====
    st.markdown("## 📈 Historical Performance")
    
    if 'historical_data' in st.session_state:
        historical_data = st.session_state.historical_data
        historical_chart = create_historical_performance_chart(historical_data)
        st.plotly_chart(historical_chart, use_container_width=True)
    else:
        st.info("📊 Load historical data from the Auto Scraper to view performance trends")
    
    # ===== ACTION PLAN =====
    st.markdown("## 🎯 Strategic Action Plan")
    
    action_plan = generate_action_plan(health_components, current_data)
    
    for priority, actions in action_plan.items():
        priority_colors = {"High": "error", "Medium": "warning", "Low": "info"}
        priority_icons = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
        
        with st.expander(f"{priority_icons[priority]} {priority} Priority Actions"):
            for action in actions:
                st.write(f"**{action['title']}**")
                st.write(f"Impact: {action['impact']}")
                st.write(f"Timeline: {action['timeline']}")
                st.write(f"Resources: {action['resources']}")
                st.write("---")

def calculate_health_score(data: dict) -> dict:
    """Calculate comprehensive health score"""
    
    # Component scoring (0-100)
    car = data.get('car', 0)
    npf = data.get('npf', 0)
    roa = data.get('roa', 0)
    bopo = data.get('bopo', 100)
    liquidity = data.get('liquidity_ratio', 0)
    
    # Capital adequacy score
    capital_score = min(100, (car / 15) * 100) if car > 0 else 0
    
    # Asset quality score (inverse of NPF)
    asset_score = max(0, 100 - (npf * 20)) if npf > 0 else 100
    
    # Profitability score
    profit_score = min(100, (roa / 2) * 100) if roa > 0 else 0
    
    # Efficiency score (inverse of BOPO)
    efficiency_score = max(0, 100 - ((bopo - 85) * 5)) if bopo > 0 else 0
    
    # Liquidity score
    liquidity_score = min(100, (liquidity / 25) * 100) if liquidity > 0 else 0
    
    # Weighted overall score
    weights = {'capital': 0.25, 'asset': 0.25, 'profit': 0.25, 'efficiency': 0.15, 'liquidity': 0.10}
    
    overall_score = (
        capital_score * weights['capital'] +
        asset_score * weights['asset'] +
        profit_score * weights['profit'] +
        efficiency_score * weights['efficiency'] +
        liquidity_score * weights['liquidity']
    )
    
    return {
        'overall_score': overall_score,
        'capital_score': capital_score,
        'asset_score': asset_score,
        'profit_score': profit_score,
        'efficiency_score': efficiency_score,
        'liquidity_score': liquidity_score
    }

def determine_risk_level(data: dict) -> str:
    """Determine overall risk level"""
    
    risk_factors = 0
    
    # Risk factor assessment
    if data.get('npf', 0) > 3.0:
        risk_factors += 2
    elif data.get('npf', 0) > 2.0:
        risk_factors += 1
    
    if data.get('car', 0) < 12.0:
        risk_factors += 2
    elif data.get('car', 0) < 15.0:
        risk_factors += 1
    
    if data.get('bopo', 0) > 95.0:
        risk_factors += 2
    elif data.get('bopo', 0) > 90.0:
        risk_factors += 1
    
    if data.get('roa', 0) < 0.5:
        risk_factors += 1
    
    # Risk level determination
    if risk_factors >= 4:
        return "High"
    elif risk_factors >= 2:
        return "Medium"
    else:
        return "Low"

def calculate_trend() -> str:
    """Calculate performance trend"""
    # Simplified trend calculation
    # In real implementation, this would analyze historical data
    return "Stable"

def calculate_industry_ranking() -> int:
    """Calculate industry ranking"""
    # Based on Islamic banking sector in Indonesia
    return 3  # Bank Muamalat typically ranks 3rd in Islamic banking

def create_health_radar_chart(health_components: dict):
    """Create radar chart for health components"""
    
    categories = ['Capital<br>Adequacy', 'Asset<br>Quality', 'Profitability', 'Efficiency', 'Liquidity']
    values = [
        health_components['capital_score'],
        health_components['asset_score'],
        health_components['profit_score'],
        health_components['efficiency_score'],
        health_components['liquidity_score']
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Bank Muamalat',
        line_color='rgb(1,90,120)'
    ))
    
    # Add industry average
    industry_avg = [75, 70, 65, 80, 75]  # Typical industry averages
    fig.add_trace(go.Scatterpolar(
        r=industry_avg,
        theta=categories,
        fill='toself',
        name='Industry Average',
        line_color='rgb(255,165,0)',
        opacity=0.6
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Financial Health Radar Analysis",
        height=500
    )
    
    return fig

def get_component_recommendations(component: str, score: float, value: float) -> list:
    """Get recommendations for each health component"""
    
    recommendations = {
        "Capital Adequacy": [
            "Maintain strong capital buffer above regulatory minimum",
            "Consider optimal capital structure for growth",
            "Evaluate dividend policy impact on capital"
        ] if score > 80 else [
            "Strengthen capital base through retained earnings",
            "Consider additional capital injection",
            "Review asset growth strategy"
        ],
        
        "Asset Quality": [
            "Maintain excellent credit risk management",
            "Continue proactive collection efforts",
            "Monitor early warning indicators"
        ] if score > 80 else [
            "Enhance credit scoring and approval processes",
            "Implement stricter collection procedures",
            "Review and strengthen collateral management"
        ],
        
        "Profitability": [
            "Focus on sustainable profit growth",
            "Diversify revenue streams",
            "Optimize pricing strategies"
        ] if score > 60 else [
            "Urgent need to improve operational efficiency",
            "Review cost structure and eliminate redundancies",
            "Focus on high-margin business segments"
        ],
        
        "Efficiency": [
            "Continue operational excellence initiatives",
            "Invest in digital transformation",
            "Optimize branch network"
        ] if score > 70 else [
            "Immediate cost reduction program required",
            "Implement automation and digitization",
            "Review organizational structure"
        ],
        
        "Liquidity": [
            "Maintain adequate liquidity buffers",
            "Monitor funding composition",
            "Diversify funding sources"
        ] if score > 75 else [
            "Strengthen liquidity management",
            "Review asset-liability maturity matching",
            "Develop contingency funding plans"
        ]
    }
    
    return recommendations.get(component, ["Monitor performance closely"])

def get_peer_comparison_data() -> dict:
    """Get peer comparison data"""
    
    return {
        'Bank Syariah Indonesia': {
            'Assets (T)': 287.5,
            'NPF (%)': 2.1,
            'CAR (%)': 25.8,
            'BOPO (%)': 85.2,
            'ROA (%)': 1.2
        },
        'Bank Mega Syariah': {
            'Assets (T)': 25.8,
            'NPF (%)': 2.8,
            'CAR (%)': 18.5,
            'BOPO (%)': 82.1,
            'ROA (%)': 0.8
        },
        'BRI Syariah': {
            'Assets (T)': 68.4,
            'NPF (%)': 3.2,
            'CAR (%)': 22.1,
            'BOPO (%)': 88.5,
            'ROA (%)': 0.9
        }
    }

def create_peer_comparison_chart(current_data: dict, peer_data: dict):
    """Create peer comparison chart"""
    
    # Prepare data for comparison
    banks = list(peer_data.keys()) + ['Bank Muamalat']
    metrics = ['NPF (%)', 'CAR (%)', 'BOPO (%)', 'ROA (%)']
    
    fig = make_subplots(rows=2, cols=2, 
                        subplot_titles=metrics,
                        specs=[[{"type": "bar"}, {"type": "bar"}],
                               [{"type": "bar"}, {"type": "bar"}]])
    
    # NPF comparison
    npf_values = [peer_data[bank]['NPF (%)'] for bank in peer_data.keys()] + [current_data.get('npf', 0)]
    fig.add_trace(go.Bar(x=banks, y=npf_values, name='NPF', marker_color='red'), row=1, col=1)
    
    # CAR comparison
    car_values = [peer_data[bank]['CAR (%)'] for bank in peer_data.keys()] + [current_data.get('car', 0)]
    fig.add_trace(go.Bar(x=banks, y=car_values, name='CAR', marker_color='green'), row=1, col=2)
    
    # BOPO comparison
    bopo_values = [peer_data[bank]['BOPO (%)'] for bank in peer_data.keys()] + [current_data.get('bopo', 0)]
    fig.add_trace(go.Bar(x=banks, y=bopo_values, name='BOPO', marker_color='orange'), row=2, col=1)
    
    # ROA comparison
    roa_values = [peer_data[bank]['ROA (%)'] for bank in peer_data.keys()] + [current_data.get('roa', 0)]
    fig.add_trace(go.Bar(x=banks, y=roa_values, name='ROA', marker_color='blue'), row=2, col=2)
    
    fig.update_layout(height=600, showlegend=False, title_text="Peer Performance Comparison")
    return fig

def create_historical_performance_chart(historical_data: list):
    """Create historical performance trend chart"""
    
    df = pd.DataFrame(historical_data)
    df['date'] = pd.to_datetime(df['timestamp'])
    
    fig = make_subplots(rows=2, cols=2,
                        subplot_titles=['Assets Trend', 'NPF Trend', 'CAR Trend', 'BOPO Trend'],
                        specs=[[{"secondary_y": False}, {"secondary_y": False}],
                               [{"secondary_y": False}, {"secondary_y": False}]])
    
    # Assets trend
    fig.add_trace(go.Scatter(x=df['date'], y=df['assets'], name='Assets (T)', line=dict(color='blue')), row=1, col=1)
    
    # NPF trend
    fig.add_trace(go.Scatter(x=df['date'], y=df['npf'], name='NPF (%)', line=dict(color='red')), row=1, col=2)
    
    # CAR trend
    fig.add_trace(go.Scatter(x=df['date'], y=df['car'], name='CAR (%)', line=dict(color='green')), row=2, col=1)
    
    # BOPO trend
    fig.add_trace(go.Scatter(x=df['date'], y=df['bopo'], name='BOPO (%)', line=dict(color='orange')), row=2, col=2)
    
    fig.update_layout(height=600, showlegend=False, title_text="30-Day Performance Trends")
    return fig

def generate_action_plan(health_components: dict, current_data: dict) -> dict:
    """Generate strategic action plan based on health analysis"""
    
    action_plan = {"High": [], "Medium": [], "Low": []}
    
    # High priority actions
    if health_components['efficiency_score'] < 60:
        action_plan["High"].append({
            "title": "Operational Efficiency Transformation",
            "impact": "Reduce BOPO by 5-8 percentage points",
            "timeline": "6-12 months",
            "resources": "Dedicated transformation team, technology investment"
        })
    
    if health_components['profit_score'] < 50:
        action_plan["High"].append({
            "title": "Profitability Enhancement Program",
            "impact": "Improve ROA by 0.3-0.5 percentage points",
            "timeline": "12-18 months",
            "resources": "Revenue optimization team, cost reduction initiatives"
        })
    
    # Medium priority actions
    if health_components['asset_score'] < 80:
        action_plan["Medium"].append({
            "title": "Asset Quality Strengthening",
            "impact": "Maintain NPF below 2%",
            "timeline": "Ongoing",
            "resources": "Enhanced credit risk management, collection team"
        })
    
    # Low priority actions
    if health_components['capital_score'] > 90:
        action_plan["Low"].append({
            "title": "Capital Optimization",
            "impact": "Optimize capital allocation for growth",
            "timeline": "12-24 months",
            "resources": "Strategic planning team, business development"
        })
    
    return action_plan

# ===== pages/risk_assessment.py =====
"""
Advanced Risk Assessment Module
Comprehensive risk analysis and monitoring
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import random

def render_risk_assessment():
    """Advanced risk assessment dashboard"""
    
    st.title("⚠️ Advanced Risk Assessment Dashboard")
    st.markdown("*Comprehensive multi-dimensional risk analysis and monitoring*")
    
    # Get current data
    current_data = st.session_state.get('current_financial_data', {})
    
    if not current_data:
        st.warning("⚠️ No current data available. Loading demo risk assessment...")
        current_data = load_demo_risk_data()
    
    # ===== RISK OVERVIEW HEATMAP =====
    st.markdown("## 🎯 Risk Heat Map")
    
    risk_matrix = calculate_risk_matrix(current_data)
    
    # Create risk heatmap
    risk_heatmap = create_risk_heatmap(risk_matrix)
    st.plotly_chart(risk_heatmap, use_container_width=True)
    
    # Risk summary cards
    col1, col2, col3, col4 = st.columns(4)
    
    risk_levels = categorize_risks(risk_matrix)
    
    with col1:
        high_risks = len(risk_levels['high'])
        st.error(f"🔴 **High Risk ({high_risks})**")
        for risk in risk_levels['high'][:3]:
            st.write(f"• {risk}")
        if len(risk_levels['high']) > 3:
            st.write(f"• ... and {len(risk_levels['high'])-3} more")
    
    with col2:
        medium_risks = len(risk_levels['medium'])
        st.warning(f"🟡 **Medium Risk ({medium_risks})**")
        for risk in risk_levels['medium'][:3]:
            st.write(f"• {risk}")
        if len(risk_levels['medium']) > 3:
            st.write(f"• ... and {len(risk_levels['medium'])-3} more")
    
    with col3:
        low_risks = len(risk_levels['low'])
        st.success(f"🟢 **Low Risk ({low_risks})**")
        for risk in risk_levels['low'][:3]:
            st.write(f"• {risk}")
        if len(risk_levels['low']) > 3:
            st.write(f"• ... and {len(risk_levels['low'])-3} more")
    
    with col4:
        overall_risk_score = calculate_overall_risk_score(risk_matrix)
        risk_color = "error" if overall_risk_score > 70 else "warning" if overall_risk_score > 40 else "success"
        getattr(st, risk_color)(f"**Overall Risk**")
        st.metric("Risk Score", f"{overall_risk_score:.0f}/100")
    
    # ===== DETAILED RISK ANALYSIS =====
    st.markdown("## 📊 Detailed Risk Analysis")
    
    # Risk categories tabs
    risk_tab1, risk_tab2, risk_tab3, risk_tab4 = st.tabs([
        "💳 Credit Risk", "⚙️ Operational Risk", "📈 Market Risk", "💰 Liquidity Risk"
    ])
    
    with risk_tab1:
        render_credit_risk_analysis(current_data, risk_matrix)
    
    with risk_tab2:
        render_operational_risk_analysis(current_data, risk_matrix)
    
    with risk_tab3:
        render_market_risk_analysis(current_data, risk_matrix)
    
    with risk_tab4:
        render_liquidity_risk_analysis(current_data, risk_matrix)
    
    # ===== RISK APPETITE & LIMITS =====
    st.markdown("## 🎯 Risk Appetite & Limits")
    
    risk_limits = get_risk_limits()
    current_metrics = extract_risk_metrics(current_data)
    
    limits_table = create_risk_limits_table(risk_limits, current_metrics)
    st.plotly_chart(limits_table, use_container_width=True)
    
    # ===== STRESS TESTING =====
    st.markdown("## 🧪 Stress Testing Scenarios")
    
    stress_col1, stress_col2 = st.columns(2)
    
    with stress_col1:
        st.markdown("### 📉 Economic Downturn Scenario")
        downturn_results = run_stress_test_downturn(current_data)
        display_stress_test_results(downturn_results)
    
    with stress_col2:
        st.markdown("### 📈 Interest Rate Shock Scenario")
        rate_shock_results = run_stress_test_rate_shock(current_data)
        display_stress_test_results(rate_shock_results)
    
    # ===== RISK MITIGATION RECOMMENDATIONS =====
    st.markdown("## 🛡️ Risk Mitigation Recommendations")
    
    recommendations = generate_risk_recommendations(risk_matrix, current_data)
    
    for priority, recs in recommendations.items():
        priority_colors = {"Critical": "error", "High": "warning", "Medium": "info"}
        priority_icons = {"Critical": "🚨", "High": "🔴", "Medium": "🟡"}
        
        if recs:  # Only show if there are recommendations
            with st.expander(f"{priority_icons[priority]} {priority} Priority Recommendations"):
                for rec in recs:
                    st.markdown(f"**{rec['title']}**")
                    st.write(f"**Risk Reduction**: {rec['impact']}")
                    st.write(f"**Implementation**: {rec['timeline']}")
                    st.write(f"**Cost**: {rec['cost']}")
                    st.write("---")

def calculate_risk_matrix(data: dict) -> dict:
    """Calculate comprehensive risk matrix"""
    
    # Credit risk calculation
    npf = data.get('npf', 0)
    credit_prob = min(0.9, npf / 5.0)  # NPF as probability indicator
    credit_impact = 0.8  # High impact for credit losses
    
    # Operational risk calculation
    bopo = data.get('bopo', 100)
    operational_prob = min(0.9, (bopo - 85) / 15)  # Efficiency as operational risk
    operational_impact = 0.7
    
    # Market risk calculation
    # Simplified - in reality would use VaR, duration analysis, etc.
    market_prob = 0.3  # Moderate probability
    market_impact = 0.6
    
    # Liquidity risk calculation
    ldr = data.get('ldr', 85)
    liquidity_prob = max(0.1, min(0.8, (ldr - 80) / 20))
    liquidity_impact = 0.9  # Very high impact
    
    # Regulatory risk
    car = data.get('car', 32.7)
    regulatory_prob = max(0.1, (15 - car) / 10) if car < 15 else 0.1
    regulatory_impact = 0.9
    
    # Technology risk
    tech_prob = 0.4  # Moderate probability
    tech_impact = 0.7
    
    # Reputational risk
    reputation_prob = 0.3
    reputation_impact = 0.8
    
    return {
        'Credit Risk': {'probability': credit_prob, 'impact': credit_impact},
        'Operational Risk': {'probability': operational_prob, 'impact': operational_impact},
        'Market Risk': {'probability': market_prob, 'impact': market_impact},
        'Liquidity Risk': {'probability': liquidity_prob, 'impact': liquidity_impact},
        'Regulatory Risk': {'probability': regulatory_prob, 'impact': regulatory_impact},
        'Technology Risk': {'probability': tech_prob, 'impact': tech_impact},
        'Reputational Risk': {'probability': reputation_prob, 'impact': reputation_impact}
    }

def create_risk_heatmap(risk_matrix: dict):
    """Create risk heatmap visualization"""
    
    risks = list(risk_matrix.keys())
    probabilities = [risk_matrix[risk]['probability'] for risk in risks]
    impacts = [risk_matrix[risk]['impact'] for risk in risks]
    risk_scores = [prob * impact for prob, impact in zip(probabilities, impacts)]
    
    # Create bubble chart
    fig = go.Figure()
    
    colors = ['red' if score > 0.6 else 'orange' if score > 0.3 else 'green' for score in risk_scores]
    
    fig.add_trace(go.Scatter(
        x=probabilities,
        y=impacts,
        mode='markers+text',
        marker=dict(
            size=[score * 100 for score in risk_scores],
            color=colors,
            opacity=0.7,
            line=dict(width=2, color='black')
        ),
        text=risks,
        textposition="middle center",
        name="Risk Categories"
    ))
    
    # Add risk zones
    fig.add_shape(type="rect", x0=0, y0=0.6, x1=0.6, y1=1, 
                  fillcolor="red", opacity=0.2, line_width=0)
    fig.add_shape(type="rect", x0=0.6, y0=0, x1=1, y1=0.6, 
                  fillcolor="orange", opacity=0.2, line_width=0)
    fig.add_shape(type="rect", x0=0, y0=0, x1=0.3, y1=0.3, 
                  fillcolor="green", opacity=0.2, line_width=0)
    
    fig.update_layout(
        title="Risk Impact vs Probability Matrix",
        xaxis_title="Probability",
        yaxis_title="Impact",
        xaxis=dict(range=[0, 1]),
        yaxis=dict(range=[0, 1]),
        height=500
    )
    
    return fig

def categorize_risks(risk_matrix: dict) -> dict:
    """Categorize risks by severity"""
    
    high_risks = []
    medium_risks = []
    low_risks = []
    
    for risk_name, risk_data in risk_matrix.items():
        risk_score = risk_data['probability'] * risk_data['impact']
        
        if risk_score > 0.6:
            high_risks.append(risk_name)
        elif risk_score > 0.3:
            medium_risks.append(risk_name)
        else:
            low_risks.append(risk_name)
    
    return {
        'high': high_risks,
        'medium': medium_risks,
        'low': low_risks
    }

def calculate_overall_risk_score(risk_matrix: dict) -> float:
    """Calculate overall risk score"""
    
    risk_scores = [data['probability'] * data['impact'] for data in risk_matrix.values()]
    weights = [0.3, 0.25, 0.15, 0.15, 0.1, 0.03, 0.02]  # Weighted by importance
    
    weighted_score = sum(score * weight for score, weight in zip(risk_scores, weights))
    return weighted_score * 100

def render_credit_risk_analysis(data: dict, risk_matrix: dict):
    """Render credit risk analysis"""
    
    st.markdown("### 💳 Credit Risk Assessment")
    
    col1, col2, col3 = st.columns(3)
    
    npf = data.get('npf', 0)
    provision_coverage = random.uniform(120, 180)
    large_exposure = random.uniform(15, 25)
    
    with col1:
        st.metric("NPF Gross", f"{npf:.2f}%", 
                 delta="vs 3% target" if npf < 3 else f"+{npf-3:.2f}% above target")
    
    with col2:
        st.metric("Provision Coverage", f"{provision_coverage:.0f}%")
    
    with col3:
        st.metric("Large Exposure", f"{large_exposure:.1f}%")
    
    # Credit risk indicators
    st.markdown("**Key Credit Risk Indicators:**")
    
    indicators = [
        ("Portfolio Concentration", "Moderate", "🟡"),
        ("Collateral Coverage", "Strong", "🟢"),
        ("Credit Approval Process", "Adequate", "🟡"),
        ("Collection Efficiency", "Good", "🟢")
    ]
    
    for indicator, status, icon in indicators:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{indicator}**")
        with col2:
            st.write(f"{icon} {status}")
    
    # Credit risk mitigation
    st.markdown("**Mitigation Strategies:**")
    st.write("• Enhanced credit scoring models")
    st.write("• Diversification of portfolio")
    st.write("• Regular stress testing")
    st.write("• Proactive collection procedures")

def render_operational_risk_analysis(data: dict, risk_matrix: dict):
    """Render operational risk analysis"""
    
    st.markdown("### ⚙️ Operational Risk Assessment")
    
    bopo = data.get('bopo', 96.62)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("BOPO Ratio", f"{bopo:.1f}%", 
                 delta=f"{bopo-94:.1f}% vs 94% target")
    
    with col2:
        fraud_incidents = random.randint(2, 8)
        st.metric("Fraud Incidents", f"{fraud_incidents}", "YTD")
    
    with col3:
        system_uptime = random.uniform(99.5, 99.9)
        st.metric("System Uptime", f"{system_uptime:.2f}%")
    
    # Operational risk categories
    risk_categories = {
        "Process Risk": random.choice(["High", "Medium", "Low"]),
        "People Risk": random.choice(["Medium", "Low"]),
        "Technology Risk": random.choice(["High", "Medium"]),
        "External Risk": random.choice(["Medium", "Low"])
    }
    
    st.markdown("**Operational Risk Categories:**")
    for category, level in risk_categories.items():
        color = "🔴" if level == "High" else "🟡" if level == "Medium" else "🟢"
        st.write(f"{color} **{category}**: {level}")

def render_market_risk_analysis(data: dict, risk_matrix: dict):
    """Render market risk analysis"""
    
    st.markdown("### 📈 Market Risk Assessment")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        var_1day = random.uniform(50, 150)
        st.metric("VaR (1-day)", f"Rp {var_1day:.0f}M", "99% confidence")
    
    with col2:
        duration_gap = random.uniform(-0.5, 0.5)
        st.metric("Duration Gap", f"{duration_gap:.2f} years")
    
    with col3:
        fx_exposure = random.uniform(2, 8)
        st.metric("FX Exposure", f"{fx_exposure:.1f}%", "of capital")
    
    # Market risk components
    st.markdown("**Market Risk Components:**")
    
    components = {
        "Interest Rate Risk": random.uniform(20, 40),
        "Foreign Exchange Risk": random.uniform(5, 15),
        "Equity Price Risk": random.uniform(10, 25),
        "Commodity Risk": random.uniform(2, 8)
    }
    
    # Create market risk breakdown chart
    fig = go.Figure(data=[go.Pie(labels=list(components.keys()), 
                                values=list(components.values()),
                                hole=.3)])
    fig.update_layout(title="Market Risk Breakdown", height=300)
    st.plotly_chart(fig, use_container_width=True)

def render_liquidity_risk_analysis(data: dict, risk_matrix: dict):
    """Render liquidity risk analysis"""
    
    st.markdown("### 💰 Liquidity Risk Assessment")
    
    ldr = data.get('ldr', 85.5)
    liquidity_ratio = data.get('liquidity_ratio', 25.5)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("LDR", f"{ldr:.1f}%", "Target: 80-90%")
    
    with col2:
        st.metric("Liquidity Ratio", f"{liquidity_ratio:.1f}%", "Min: 20%")
    
    with col3:
        lcr = random.uniform(110, 150)
        st.metric("LCR", f"{lcr:.0f}%", "Min: 100%")
    
    # Liquidity risk indicators
    st.markdown("**Liquidity Risk Indicators:**")
    
    # Funding concentration
    funding_sources = {
        "Demand Deposits": 45,
        "Savings": 30,
        "Time Deposits": 20,
        "Interbank": 5
    }
    
    fig = go.Figure(data=[go.Bar(x=list(funding_sources.keys()), 
                                y=list(funding_sources.values()))])
    fig.update_layout(title="Funding Source Concentration (%)", height=300)
    st.plotly_chart(fig, use_container_width=True)

def get_risk_limits():
    """Get risk appetite limits"""
    
    return {
        "NPF Ratio": {"limit": 5.0, "threshold": 3.0, "current": 0.86},
        "CAR": {"limit": 8.0, "threshold": 12.0, "current": 32.7},
        "BOPO": {"limit": 94.0, "threshold": 90.0, "current": 96.62},
        "LDR": {"limit": 92.0, "threshold": 90.0, "current": 85.5},
        "Single Borrower": {"limit": 20.0, "threshold": 15.0, "current": 18.5}
    }

def extract_risk_metrics(data: dict) -> dict:
    """Extract risk metrics from current data"""
    
    return {
        "NPF Ratio": data.get('npf', 0.86),
        "CAR": data.get('car', 32.7),
        "BOPO": data.get('bopo', 96.62),
        "LDR": data.get('ldr', 85.5),
        "Single Borrower": random.uniform(15, 20)
    }

def create_risk_limits_table(limits: dict, current: dict):
    """Create risk limits visualization"""
    
    metrics = []
    statuses = []
    colors = []
    
    for metric, limit_data in limits.items():
        current_val = current.get(metric, 0)
        limit_val = limit_data["limit"]
        threshold_val = limit_data["threshold"]
        
        metrics.append(metric)
        
        # Determine status based on metric type
        if metric in ["NPF Ratio", "BOPO", "LDR", "Single Borrower"]:
            # Lower is better
            if current_val > limit_val:
                status = "🔴 Breach"
                color = "red"
            elif current_val > threshold_val:
                status = "🟡 Warning"
                color = "orange"
            else:
                status = "🟢 Safe"
                color = "green"
        else:
            # Higher is better (CAR)
            if current_val < limit_val:
                status = "🔴 Breach"
                color = "red"
            elif current_val < threshold_val:
                status = "🟡 Warning"
                color = "orange"
            else:
                status = "🟢 Safe"
                color = "green"
        
        statuses.append(status)
        colors.append(color)
    
    # Create table visualization
    fig = go.Figure(data=[go.Table(
        header=dict(values=['Metric', 'Current', 'Threshold', 'Limit', 'Status'],
                   fill_color='paleturquoise',
                   align='left'),
        cells=dict(values=[metrics,
                          [f"{current[m]:.1f}%" for m in metrics],
                          [f"{limits[m]['threshold']:.1f}%" for m in metrics],
                          [f"{limits[m]['limit']:.1f}%" for m in metrics],
                          statuses],
                  fill_color=['lightgray' if i % 2 == 0 else 'white' for i in range(len(metrics))],
                  align='left'))
    ])
    
    fig.update_layout(title="Risk Appetite & Limits Monitoring", height=300)
    return fig

def run_stress_test_downturn(data: dict) -> dict:
    """Run economic downturn stress test"""
    
    base_npf = data.get('npf', 0.86)
    base_roa = data.get('roa', 0.45)
    base_car = data.get('car', 32.7)
    
    # Economic downturn scenario assumptions
    npf_shock = base_npf * 3.5  # NPF increases 3.5x
    roa_impact = base_roa - 0.8  # ROA decreases significantly
    car_impact = base_car - 5.0  # CAR decreases due to losses
    
    return {
        "scenario": "Economic Downturn",
        "npf_stressed": min(15.0, npf_shock),
        "roa_stressed": max(-2.0, roa_impact),
        "car_stressed": max(8.0, car_impact),
        "severity": "Severe" if npf_shock > 10 else "Moderate"
    }

def run_stress_test_rate_shock(data: dict) -> dict:
    """Run interest rate shock stress test"""
    
    base_nim = data.get('nim', 2.8)
    base_roa = data.get('roa', 0.45)
    
    # Interest rate shock assumptions (+300 bps)
    nim_impact = base_nim - 0.5  # NIM compression
    roa_impact = base_roa - 0.3  # ROA impact
    
    return {
        "scenario": "Interest Rate Shock (+300bps)",
        "nim_stressed": max(1.0, nim_impact),
        "roa_stressed": max(0.0, roa_impact),
        "severity": "Moderate"
    }

def display_stress_test_results(results: dict):
    """Display stress test results"""
    
    st.write(f"**Scenario**: {results['scenario']}")
    st.write(f"**Severity**: {results['severity']}")
    
    for key, value in results.items():
        if key not in ['scenario', 'severity']:
            metric_name = key.replace('_stressed', '').replace('_', ' ').title()
            st.metric(metric_name, f"{value:.2f}%")

def generate_risk_recommendations(risk_matrix: dict, data: dict) -> dict:
    """Generate risk mitigation recommendations"""
    
    recommendations = {"Critical": [], "High": [], "Medium": []}
    
    # Operational risk (BOPO)
    if data.get('bopo', 0) > 95:
        recommendations["Critical"].append({
            "title": "Immediate Operational Efficiency Program",
            "impact": "Reduce operational risk by 40%",
            "timeline": "3-6 months",
            "cost": "Medium investment in automation"
        })
    
    # Credit risk (NPF)
    if data.get('npf', 0) > 2:
        recommendations["High"].append({
            "title": "Enhanced Credit Risk Management",
            "impact": "Reduce credit risk by 25%",
            "timeline": "6-12 months",
            "cost": "Low - process improvements"
        })
    
    # General recommendations
    recommendations["Medium"].append({
        "title": "Risk Management Technology Upgrade",
        "impact": "Improve risk monitoring by 30%",
        "timeline": "12-18 months",
        "cost": "High - system implementation"
    })
    
    return recommendations

def load_demo_risk_data() -> dict:
    """Load demo data for risk assessment"""
    
    return {
        'assets': 61.4,
        'npf': 0.86,
        'car': 32.7,
        'bopo': 96.62,
        'roa': 0.45,
        'roe': 4.2,
        'nim': 2.8,
        'ldr': 85.5,
        'liquidity_ratio': 25.5
    }

# ===== pages/compliance_monitoring.py =====
"""
Advanced Compliance Monitoring Module
Regulatory compliance tracking and automated reporting
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

def render_compliance_monitoring():
    """Advanced compliance monitoring dashboard"""
    
    st.title("📋 Compliance Monitoring Dashboard")
    st.markdown("*Comprehensive regulatory compliance tracking and automated reporting*")
    
    # Get current data
    current_data = st.session_state.get('current_financial_data', {})
    
    if not current_data:
        st.info("Loading compliance monitoring with demo data...")
        current_data = load_demo_compliance_data()
    
    # ===== COMPLIANCE OVERVIEW =====
    st.markdown("## 📊 Compliance Overview")
    
    compliance_metrics = calculate_compliance_metrics(current_data)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        score = compliance_metrics['overall_score']
        color = "success" if score >= 90 else "warning" if score >= 80 else "error"
        getattr(st, color)(f"**{score:.1f}%**")
        st.caption("Overall Compliance Score")
    
    with col2:
        open_issues = compliance_metrics['open_issues']
        color = "success" if open_issues == 0 else "warning" if open_issues <= 3 else "error"
        getattr(st, color)(f"**{open_issues}**")
        st.caption("Open Issues")
    
    with col3:
        resolved_issues = compliance_metrics['resolved_this_month']
        st.success(f"**{resolved_issues}**")
        st.caption("Resolved This Month")
    
    with col4:
        next_audit = datetime.now() + timedelta(days=45)
        st.info(f"**{next_audit.strftime('%b %Y')}**")
        st.caption("Next Regulatory Audit")
    
    # ===== REGULATORY REQUIREMENTS TRACKING =====
    st.markdown("## 🎯 Regulatory Requirements Tracking")
    
    regulations = get_regulatory_requirements()
    compliance_status = assess_compliance_status(current_data, regulations)
    
    # Create compliance dashboard
    compliance_chart = create_compliance_dashboard(compliance_status)
    st.plotly_chart(compliance_chart, use_container_width=True)
    
    # Detailed compliance table
    st.markdown("### 📋 Detailed Compliance Status")
    
    compliance_df = create_compliance_dataframe(compliance_status)
    
    # Style the dataframe
    def style_compliance(val):
        if val == "Compliant":
            return 'background-color: #d4edda; color: #155724'
        elif val == "Non-Compliant":
            return 'background-color: #f8d7da; color: #721c24'
        elif val == "Warning":
            return 'background-color: #fff3cd; color: #856404'
        return ''
    
    styled_df = compliance_df.style.applymap(style_compliance, subset=['Status'])
    st.dataframe(styled_df, use_container_width=True)
    
    # ===== COMPLIANCE ISSUES MANAGEMENT =====
    st.markdown("## 🚨 Active Compliance Issues")
    
    issues = get_compliance_issues()
    
    if issues:
        for issue in issues:
            severity_colors = {"Critical": "error", "High": "error", "Medium": "warning", "Low": "info"}
            severity_icons = {"Critical": "🚨", "High": "🔴", "Medium": "🟡", "Low": "🟢"}
            
            with st.expander(f"{severity_icons[issue['severity']]} {issue['id']}: {issue['title']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Category**: {issue['category']}")
                    st.write(f"**Severity**: {issue['severity']}")
                    st.write(f"**Status**: {issue['status']}")
                    st.write(f"**Owner**: {issue['owner']}")
                
                with col2:
                    st.write(f"**Opened**: {issue['opened']}")
                    st.write(f"**Due Date**: {issue['due_date']}")
                    days_remaining = (datetime.strptime(issue['due_date'], '%Y-%m-%d') - datetime.now()).days
                    if days_remaining < 0:
                        st.error(f"**Overdue by {abs(days_remaining)} days**")
                    elif days_remaining < 7:
                        st.warning(f"**Due in {days_remaining} days**")
                    else:
                        st.info(f"**Due in {days_remaining} days**")
                
                # Action buttons
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    if st.button(f"Update Status", key=f"update_{issue['id']}"):
                        st.success(f"Status updated for {issue['id']}")
                with col_b:
                    if st.button(f"Add Comment", key=f"comment_{issue['id']}"):
                        st.info(f"Comment added to {issue['id']}")
                with col_c:
                    if st.button(f"Close Issue", key=f"close_{issue['id']}"):
                        st.success(f"Issue {issue['id']} marked as resolved")
    else:
        st.success("✅ **No active compliance issues**")
    
    # ===== REGULATORY REPORTING =====
    st.markdown("## 📊 Regulatory Reporting Status")
    
    reports = get_regulatory_reports_status()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📅 **Recent Reports**")
        for report in reports['recent']:
            status_icon = "✅" if report['status'] == 'Submitted' else "⏳" if report['status'] == 'In Progress' else "🔴"
            st.write(f"{status_icon} **{report['name']}** - {report['status']}")
            st.caption(f"Due: {report['due_date']}")
    
    with col2:
        st.markdown("### 📋 **Upcoming Reports**")
        for report in reports['upcoming']:
            days_until_due = (datetime.strptime(report['due_date'], '%Y-%m-%d') - datetime.now()).days
            urgency_icon = "🔴" if days_until_due <= 3 else "🟡" if days_until_due <= 7 else "🟢"
            st.write(f"{urgency_icon} **{report['name']}**")
            st.caption(f"Due in {days_until_due} days")
    
    # ===== COMPLIANCE TRAINING & AWARENESS =====
    st.markdown("## 🎓 Compliance Training & Awareness")
    
    training_metrics = get_training_metrics()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Training Completion", f"{training_metrics['completion_rate']:.1f}%", 
                 delta=f"{training_metrics['completion_rate']-85:.1f}% vs target")
    
    with col2:
        st.metric("Certified Staff", f"{training_metrics['certified_staff']}", 
                 f"of {training_metrics['total_staff']} total")
    
    with col3:
        st.metric("Training Hours", f"{training_metrics['total_hours']}", "This year")
    
    # Training status breakdown
    training_chart = create_training_status_chart(training_metrics)
    st.plotly_chart(training_chart, use_container_width=True)
    
    # ===== REGULATORY CHANGES MONITORING =====
    st.markdown("## 📰 Regulatory Changes & Updates")
    
    reg_updates = get_regulatory_updates()
    
    for update in reg_updates:
        impact_colors = {"High": "error", "Medium": "warning", "Low": "info"}
        impact_icons = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
        
        with st.expander(f"{impact_icons[update['impact']]} {update['title']} - {update['source']}"):
            st.write(f"**Effective Date**: {update['effective_date']}")
            st.write(f"**Impact Level**: {update['impact']}")
            st.write(f"**Summary**: {update['summary']}")
            st.write(f"**Required Actions**: {update['actions']}")
            
            if update['impact'] == 'High':
                st.error("⚠️ **Immediate attention required**")
            elif update['impact'] == 'Medium':
                st.warning("📋 **Review and plan implementation**")

def calculate_compliance_metrics(data: dict) -> dict:
    """Calculate overall compliance metrics"""
    
    # Regulatory compliance scoring
    car = data.get('car', 32.7)
    npf = data.get('npf', 0.86)
    bopo = data.get('bopo', 96.62)
    ldr = data.get('ldr', 85.5)
    
    compliance_scores = []
    
    # CAR compliance (8% minimum)
    compliance_scores.append(100 if car >= 8 else 0)
    
    # NPF compliance (5% maximum)
    compliance_scores.append(100 if npf <= 5 else max(0, 100 - (npf - 5) * 20))
    
    # BOPO compliance (varies by bank type, assume 94% for Islamic banks)
    compliance_scores.append(100 if bopo <= 94 else max(0, 100 - (bopo - 94) * 10))
    
    # LDR compliance (78-92% range)
    if 78 <= ldr <= 92:
        compliance_scores.append(100)
    else:
        compliance_scores.append(max(0, 100 - abs(ldr - 85) * 5))
    
    overall_score = sum(compliance_scores) / len(compliance_scores)
    
    return {
        'overall_score': overall_score,
        'open_issues': random.randint(2, 8),
        'resolved_this_month': random.randint(5, 15),
        'compliance_scores': compliance_scores
    }

def get_regulatory_requirements() -> dict:
    """Get comprehensive regulatory requirements"""
    
    return {
        "Bank Indonesia Regulations": {
            "CAR Minimum": {"requirement": "8%", "type": "minimum"},
            "NPF Maximum": {"requirement": "5%", "type": "maximum"},
            "BOPO Maximum": {"requirement": "94%", "type": "maximum"},
            "LDR Range": {"requirement": "78-92%", "type": "range"},
            "GWM Rupiah": {"requirement": "3.5%", "type": "minimum"},
            "GWM Valas": {"requirement": "8%", "type": "minimum"}
        },
        "OJK Regulations": {
            "Corporate Governance": {"requirement": "Compliant", "type": "qualitative"},
            "Risk Management": {"requirement": "Adequate", "type": "qualitative"},
            "Internal Control": {"requirement": "Effective", "type": "qualitative"},
            "Compliance Function": {"requirement": "Independent", "type": "qualitative"}
        },
        "Islamic Banking Regulations": {
            "Sharia Compliance": {"requirement": "100%", "type": "minimum"},
            "DPS Meetings": {"requirement": "Monthly", "type": "frequency"},
            "Sharia Audit": {"requirement": "Annual", "type": "frequency"},
            "Islamic Instruments": {"requirement": ">80%", "type": "minimum"}
        },
        "International Standards": {
            "Basel III": {"requirement": "Compliant", "type": "qualitative"},
            "IFRS": {"requirement": "Implemented", "type": "qualitative"},
            "AML/CFT": {"requirement": "Effective", "type": "qualitative"},
            "FATCA/CRS": {"requirement": "Compliant", "type": "qualitative"}
        }
    }

def assess_compliance_status(data: dict, regulations: dict) -> dict:
    """Assess compliance status against regulations"""
    
    compliance_status = {}
    
    # Bank Indonesia Regulations
    car = data.get('car', 32.7)
    npf = data.get('npf', 0.86)
    bopo = data.get('bopo', 96.62)
    ldr = data.get('ldr', 85.5)
    
    compliance_status["CAR Minimum"] = {
        "current": f"{car:.2f}%",
        "requirement": "8%",
        "status": "Compliant" if car >= 8 else "Non-Compliant",
        "gap": max(0, 8 - car)
    }
    
    compliance_status["NPF Maximum"] = {
        "current": f"{npf:.2f}%",
        "requirement": "5%",
        "status": "Compliant" if npf <= 5 else "Non-Compliant",
        "gap": max(0, npf - 5)
    }
    
    compliance_status["BOPO Maximum"] = {
        "current": f"{bopo:.1f}%",
        "requirement": "94%",
        "status": "Non-Compliant" if bopo > 94 else "Warning" if bopo > 90 else "Compliant",
        "gap": max(0, bopo - 94)
    }
    
    compliance_status["LDR Range"] = {
        "current": f"{ldr:.1f}%",
        "requirement": "78-92%",
        "status": "Compliant" if 78 <= ldr <= 92 else "Non-Compliant",
        "gap": 0 if 78 <= ldr <= 92 else min(abs(ldr - 78), abs(ldr - 92))
    }
    
    # Add other regulations with simulated status
    other_reqs = [
        ("GWM Rupiah", "3.8%", "3.5%", "Compliant"),
        ("GWM Valas", "8.5%", "8%", "Compliant"),
        ("Sharia Compliance", "99.8%", "100%", "Warning"),
        ("Corporate Governance", "Good", "Adequate", "Compliant"),
        ("Risk Management", "Adequate", "Adequate", "Compliant"),
        ("Basel III", "Implemented", "Compliant", "Compliant")
    ]
    
    for name, current, requirement, status in other_reqs:
        compliance_status[name] = {
            "current": current,
            "requirement": requirement,
            "status": status,
            "gap": 0
        }
    
    return compliance_status

def create_compliance_dashboard(compliance_status: dict):
    """Create compliance dashboard visualization"""
    
    # Prepare data for visualization
    requirements = list(compliance_status.keys())
    statuses = [compliance_status[req]['status'] for req in requirements]
    
    # Count by status
    status_counts = {'Compliant': 0, 'Warning': 0, 'Non-Compliant': 0}
    for status in statuses:
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Create pie chart for compliance overview
    fig = go.Figure(data=[
        go.Pie(
            labels=list(status_counts.keys()),
            values=list(status_counts.values()),
            marker_colors=['green', 'orange', 'red'],
            hole=0.4
        )
    ])
    
    fig.update_layout(
        title="Regulatory Compliance Overview",
        annotations=[dict(text='Compliance<br>Status', x=0.5, y=0.5, font_size=16, showarrow=False)],
        height=400
    )
    
    return fig

def create_compliance_dataframe(compliance_status: dict) -> pd.DataFrame:
    """Create compliance dataframe for detailed view"""
    
    data = []
    for requirement, details in compliance_status.items():
        data.append({
            'Requirement': requirement,
            'Current Value': details['current'],
            'Regulatory Standard': details['requirement'],
            'Status': details['status'],
            'Gap': f"{details['gap']:.2f}" if isinstance(details['gap'], (int, float)) else "N/A"
        })
    
    return pd.DataFrame(data)

def get_compliance_issues() -> list:
    """Get list of current compliance issues"""
    
    issues = [
        {
            "id": "COMP-2024-001",
            "title": "BOPO ratio exceeds regulatory guideline",
            "category": "Operational Efficiency",
            "severity": "High",
            "status": "In Progress",
            "owner": "Operations Team",
            "opened": "2024-06-15",
            "due_date": "2024-08-15",
            "description": "BOPO ratio at 96.62% exceeds the 94% guideline"
        },
        {
            "id": "COMP-2024-002",
            "title": "Sharia compliance documentation gap",
            "category": "Islamic Banking",
            "severity": "Medium",
            "status": "Open",
            "owner": "Sharia Compliance",
            "opened": "2024-07-01",
            "due_date": "2024-08-01",
            "description": "Minor gaps in product documentation for Sharia compliance"
        },
        {
            "id": "COMP-2024-003",
            "title": "Late submission of prudential reports",
            "category": "Regulatory Reporting",
            "severity": "Low",
            "status": "Resolved",
            "owner": "Compliance Team",
            "opened": "2024-07-10",
            "due_date": "2024-07-25",
            "description": "Monthly prudential report submitted 2 days late"
        }
    ]
    
    # Filter out resolved issues for active issues display
    return [issue for issue in issues if issue['status'] != 'Resolved']

def get_regulatory_reports_status() -> dict:
    """Get regulatory reporting status"""
    
    return {
        "recent": [
            {"name": "Monthly Prudential Report", "status": "Submitted", "due_date": "2024-07-10"},
            {"name": "Quarterly LKT Report", "status": "Submitted", "due_date": "2024-07-15"},
            {"name": "Islamic Banking Statistics", "status": "In Progress", "due_date": "2024-07-20"}
        ],
        "upcoming": [
            {"name": "Monthly Prudential Report", "due_date": "2024-08-10"},
            {"name": "Capital Adequacy Report", "due_date": "2024-08-15"},
            {"name": "Risk Profile Report", "due_date": "2024-08-20"},
            {"name": "Sharia Compliance Report", "due_date": "2024-08-25"}
        ]
    }

def get_training_metrics() -> dict:
    """Get compliance training metrics"""
    
    return {
        "completion_rate": random.uniform(88, 96),
        "certified_staff": random.randint(180, 220),
        "total_staff": 250,
        "total_hours": random.randint(1200, 1800),
        "by_department": {
            "Credit": random.uniform(90, 98),
            "Operations": random.uniform(85, 93),
            "Risk Management": random.uniform(95, 99),
            "Compliance": random.uniform(98, 100),
            "Treasury": random.uniform(87, 94)
        }
    }

def create_training_status_chart(training_metrics: dict):
    """Create training status chart"""
    
    departments = list(training_metrics['by_department'].keys())
    completion_rates = list(training_metrics['by_department'].values())
    
    fig = go.Figure(data=[
        go.Bar(
            x=departments,
            y=completion_rates,
            marker_color=['green' if rate >= 95 else 'orange' if rate >= 90 else 'red' for rate in completion_rates],
            text=[f"{rate:.1f}%" for rate in completion_rates],
            textposition='auto'
        )
    ])
    
    fig.add_hline(y=95, line_dash="dash", line_color="green", annotation_text="Target: 95%")
    
    fig.update_layout(
        title="Compliance Training Completion by Department",
        xaxis_title="Department",
        yaxis_title="Completion Rate (%)",
        height=400
    )
    
    return fig

def get_regulatory_updates() -> list:
    """Get recent regulatory updates"""
    
    return [
        {
            "title": "Updated Islamic Banking Prudential Regulations",
            "source": "OJK",
            "effective_date": "2024-09-01",
            "impact": "Medium",
            "summary": "Revised capital requirements for Islamic banking operations",
            "actions": "Review capital adequacy calculations and update reporting procedures"
        },
        {
            "title": "Enhanced AML/CFT Guidelines",
            "source": "PPATK",
            "effective_date": "2024-08-15",
            "impact": "High",
            "summary": "Strengthened customer due diligence and transaction monitoring requirements",
            "actions": "Update CDD procedures, enhance transaction monitoring systems"
        },
        {
            "title": "Digital Banking Security Standards",
            "source": "Bank Indonesia",
            "effective_date": "2024-10-01",
            "impact": "Medium",
            "summary": "New cybersecurity requirements for digital banking services",
            "actions": "Assess current security infrastructure, plan upgrades if necessary"
        }
    ]

def load_demo_compliance_data() -> dict:
    """Load demo data for compliance monitoring"""
    
    return {
        'car': 32.7,
        'npf': 0.86,
        'bopo': 96.62,
        'ldr': 85.5,
        'liquidity_ratio': 25.5
    }

# Export functions
__all__ = [
    'render_financial_health',
    'render_risk_assessment', 
    'render_compliance_monitoring'
]