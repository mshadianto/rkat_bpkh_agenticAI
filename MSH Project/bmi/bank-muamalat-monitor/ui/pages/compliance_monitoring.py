"""
Compliance Monitoring Page for Bank Muamalat Health Monitoring
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
from typing import Optional, Any

def render(orchestrator: Optional[Any] = None):
    """Render the compliance monitoring page"""
    
    try:
        st.title("📋 Compliance & GRC Monitoring")
        st.markdown("### Governance, Risk, and Compliance oversight")
        
        # Compliance overview
        render_compliance_overview()
        
        # Regulatory compliance
        render_regulatory_compliance()
        
        # GRC metrics
        render_grc_metrics()
        
        # Audit findings
        render_audit_findings()
        
    except Exception as e:
        st.error(f"Error rendering compliance page: {str(e)}")
        st.info("Please try refreshing the page or contact support if the issue persists.")

def render_compliance_overview():
    """Render compliance overview"""
    st.markdown("## 📊 Compliance Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Score", "85%", "2%")
    with col2:
        st.metric("Regulatory Compliance", "92%", "1%")
    with col3:
        st.metric("Risk Management", "78%", "3%")
    with col4:
        st.metric("Governance", "88%", "1%")
    
    # Compliance trends
    months = pd.date_range(end=datetime.now(), periods=12, freq='M')
    compliance_data = pd.DataFrame({
        'Month': months,
        'Regulatory': [90, 91, 89, 92, 93, 91, 92, 94, 93, 91, 92, 92],
        'Risk': [75, 76, 74, 77, 78, 76, 77, 79, 78, 76, 77, 78],
        'Governance': [85, 86, 84, 87, 88, 86, 87, 89, 88, 86, 87, 88]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=compliance_data['Month'], y=compliance_data['Regulatory'], name='Regulatory'))
    fig.add_trace(go.Scatter(x=compliance_data['Month'], y=compliance_data['Risk'], name='Risk'))
    fig.add_trace(go.Scatter(x=compliance_data['Month'], y=compliance_data['Governance'], name='Governance'))
    
    fig.update_layout(
        title="Compliance Trends", 
        yaxis_title="Score (%)",
        xaxis_title="Month",
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

def render_regulatory_compliance():
    """Render regulatory compliance status"""
    st.markdown("## 🏛️ Regulatory Compliance")
    
    try:
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("CAR Compliance", "✅ PASS", "29.42% > 8%")
            st.metric("NPF Compliance", "⚠️ WATCH", "3.99% near 5%")
            st.metric("BOPO Compliance", "❌ FAIL", "98.5% > 94%")
            st.metric("PDN Compliance", "✅ PASS", "85% < 92%")
            
        with col2:
            # Compliance by regulation
            regulations = pd.DataFrame({
                'Regulation': ['Basel III', 'OJK Regulation', 'BI Regulation', 'Anti-Money Laundering'],
                'Status': ['Compliant', 'Compliant', 'Non-Compliant', 'Compliant'],
                'Score': [95, 92, 65, 88]
            })
            
            color_map = {'Compliant': 'green', 'Non-Compliant': 'red'}
            fig = px.bar(regulations, x='Regulation', y='Score', color='Status', 
                        color_discrete_map=color_map, title='Regulatory Compliance Status')
            
            fig.update_layout(
                yaxis=dict(range=[0, 100], title="Compliance Score (%)"),
                xaxis_title="Regulations"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
    except Exception as e:
        st.error(f"Error rendering regulatory compliance: {str(e)}")
        # Fallback display
        st.info("Regulatory Status: CAR ✅, NPF ⚠️, BOPO ❌, PDN ✅")

def render_grc_metrics():
    """Render GRC metrics"""
    st.markdown("## 🛡️ GRC Metrics")
    
    try:
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Board Meetings", "12", "Regular")
            st.metric("Risk Committee", "24", "Monthly")
            st.metric("Audit Committee", "18", "Quarterly")
            st.metric("Compliance Training", "95%", "5%")
            
        with col2:
            # GRC framework maturity
            grc_maturity = pd.DataFrame({
                'Area': ['Risk Management', 'Compliance', 'Governance', 'Internal Audit'],
                'Maturity Level': [3, 4, 3, 3]  # 1-5 scale
            })
            
            fig = px.bar(grc_maturity, x='Area', y='Maturity Level', 
                        title='GRC Framework Maturity',
                        color='Maturity Level',
                        color_continuous_scale='Blues')
            
            # Update layout instead of update_yaxis
            fig.update_layout(
                yaxis=dict(range=[0, 5], title="Maturity Level (1-5)"),
                xaxis_title="GRC Areas",
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
    except Exception as e:
        st.error(f"Error rendering GRC metrics: {str(e)}")
        # Fallback display
        st.info("GRC Metrics: Risk Management (3/5), Compliance (4/5), Governance (3/5), Internal Audit (3/5)")

def render_audit_findings():
    """Render audit findings"""
    st.markdown("## 🔍 Audit Findings")
    
    try:
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Open Findings", "23", "-5")
            st.metric("High Risk", "3", "-1")
            st.metric("Medium Risk", "12", "-2")
            st.metric("Low Risk", "8", "-2")
            
        with col2:
            # Audit findings by category
            findings = pd.DataFrame({
                'Category': ['Credit Risk', 'Operational Risk', 'Compliance', 'IT Security'],
                'Count': [8, 7, 5, 3]
            })
            
            fig = px.pie(findings, values='Count', names='Category', 
                        title='Audit Findings by Category',
                        color_discrete_sequence=px.colors.qualitative.Set3)
            
            fig.update_layout(showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
        
        # Recent audit actions
        st.markdown("### Recent Audit Actions")
        audit_actions = pd.DataFrame({
            'Finding': ['BOPO Efficiency', 'NPF Monitoring', 'IT Security'],
            'Priority': ['High', 'Medium', 'High'],
            'Status': ['In Progress', 'Completed', 'Planned'],
            'Due Date': ['2024-08-15', '2024-07-30', '2024-09-01']
        })
        
        # Color code the dataframe
        def highlight_priority(val):
            if val == 'High':
                return 'background-color: #ffcccc'
            elif val == 'Medium':
                return 'background-color: #ffffcc'
            return ''
        
        styled_df = audit_actions.style.applymap(highlight_priority, subset=['Priority'])
        st.dataframe(styled_df, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error rendering audit findings: {str(e)}")
        # Fallback display
        st.info("Audit Summary: 23 Open Findings (3 High, 12 Medium, 8 Low Risk)")

# Add helper function for error handling
def safe_render_chart(chart_func, fallback_message, *args, **kwargs):
    """Safely render chart with fallback"""
    try:
        return chart_func(*args, **kwargs)
    except Exception as e:
        st.error(f"Chart rendering error: {str(e)}")
        st.info(fallback_message)
        return None

# Export the render function
__all__ = ['render']