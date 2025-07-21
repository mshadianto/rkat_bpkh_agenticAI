# ===== pages/__init__.py =====
"""
Pages package initialization
"""

__version__ = "2.0.0"

# ===== pages/financial_health.py =====
"""
Financial Health Assessment Module
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

def render_financial_health():
    """Render comprehensive financial health assessment"""
    
    st.title("💰 Financial Health Assessment")
    st.markdown("*Comprehensive analysis of Bank Muamalat's financial performance and stability*")
    
    # Health Score Overview
    st.markdown("## 🎯 Overall Health Score")
    
    # Calculate health score based on key metrics
    health_components = {
        "Capital Adequacy": {"score": 85, "weight": 0.25, "status": "Strong"},
        "Asset Quality": {"score": 60, "weight": 0.25, "status": "Needs Attention"},
        "Profitability": {"score": 45, "weight": 0.25, "status": "Below Target"},
        "Liquidity": {"score": 80, "weight": 0.25, "status": "Adequate"}
    }
    
    overall_score = sum(comp["score"] * comp["weight"] for comp in health_components.values())
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Health score gauge
        if overall_score >= 80:
            color = "green"
            status = "Excellent"
        elif overall_score >= 70:
            color = "orange"
            status = "Good"
        elif overall_score >= 60:
            color = "yellow"
            status = "Fair"
        else:
            color = "red"
            status = "Poor"
        
        st.metric("Health Score", f"{overall_score:.0f}/100", f"Status: {status}")
    
    with col2:
        st.metric("Risk Level", "Medium", "⚠️ Monitor closely")
    
    with col3:
        st.metric("Trend", "Declining", "📉 -5 points (QoQ)")
    
    # Detailed Component Analysis
    st.markdown("## 📊 Component Analysis")
    
    for component, data in health_components.items():
        with st.expander(f"{component} - Score: {data['score']}/100 ({data['status']})"):
            col1, col2 = st.columns(2)
            
            with col1:
                # Progress bar for component score
                progress = data['score'] / 100
                st.progress(progress)
                st.write(f"**Current Score**: {data['score']}/100")
                st.write(f"**Weight in Overall**: {data['weight']*100:.0f}%")
                st.write(f"**Status**: {data['status']}")
            
            with col2:
                # Component-specific details
                if component == "Capital Adequacy":
                    st.write("**Key Metrics:**")
                    st.write("• CAR: 29.42% (Target: >12%)")
                    st.write("• Tier 1 Capital: 25.8%")
                    st.write("• Core Capital: 23.5%")
                    
                elif component == "Asset Quality":
                    st.write("**Key Metrics:**")
                    st.write("• NPF Gross: 3.99% (Target: <3%)")
                    st.write("• NPF Net: 2.1%")
                    st.write("• Provision Coverage: 75%")
                    
                elif component == "Profitability":
                    st.write("**Key Metrics:**")
                    st.write("• ROA: 0.45% (Target: >1%)")
                    st.write("• ROE: 4.2% (Target: >15%)")
                    st.write("• NIM: 2.8%")
                    
                elif component == "Liquidity":
                    st.write("**Key Metrics:**")
                    st.write("• LDR: 85.5% (Target: 80-90%)")
                    st.write("• Liquidity Ratio: 25.5%")
                    st.write("• Quick Ratio: 15.2%")
    
    # Recommendations
    st.markdown("## 📋 Health Improvement Recommendations")
    
    recommendations = [
        {
            "priority": "High",
            "area": "Operational Efficiency",
            "issue": "BOPO ratio at 98.5% significantly above industry benchmark",
            "action": "Implement cost reduction program and process automation",
            "timeline": "6 months",
            "impact": "Could improve health score by 15 points"
        },
        {
            "priority": "High", 
            "area": "Asset Quality",
            "issue": "NPF trend increasing towards regulatory threshold",
            "action": "Strengthen credit risk management and collection procedures",
            "timeline": "3 months",
            "impact": "Could improve health score by 10 points"
        },
        {
            "priority": "Medium",
            "area": "Revenue Generation",
            "issue": "ROA below industry average",
            "action": "Focus on fee-based income and margin optimization",
            "timeline": "9 months",
            "impact": "Could improve health score by 8 points"
        }
    ]
    
    for i, rec in enumerate(recommendations, 1):
        priority_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}[rec["priority"]]
        
        with st.expander(f"{priority_color} Priority {i}: {rec['area']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Issue**: {rec['issue']}")
                st.write(f"**Recommended Action**: {rec['action']}")
            
            with col2:
                st.write(f"**Timeline**: {rec['timeline']}")
                st.write(f"**Potential Impact**: {rec['impact']}")
                st.write(f"**Priority**: {rec['priority']}")
    
    # Health Trend Chart
    st.markdown("## 📈 Health Score Trend")
    
    # Sample historical data
    months = ['Jan 2024', 'Feb 2024', 'Mar 2024', 'Apr 2024', 'May 2024', 'Jun 2024']
    health_scores = [78, 76, 74, 72, 70, 67.5]
    
    fig = px.line(x=months, y=health_scores, title="Health Score Trend (6 Months)")
    fig.update_traces(line=dict(color='red', width=3))
    fig.add_hline(y=70, line_dash="dash", line_color="orange", annotation_text="Target: 70")
    fig.update_layout(yaxis_title="Health Score", xaxis_title="Month")
    st.plotly_chart(fig, use_container_width=True)

# ===== pages/risk_assessment.py =====
"""
Risk Assessment Module
"""

import streamlit as st
import numpy as np

def render_risk_assessment():
    """Render comprehensive risk assessment dashboard"""
    
    st.title("⚠️ Risk Assessment Dashboard")
    st.markdown("*Comprehensive risk monitoring, analysis and management*")
    
    # Risk Overview Heatmap
    st.markdown("## 🎯 Risk Heat Map")
    
    risk_matrix = {
        "Credit Risk": {"probability": 0.7, "impact": 0.8, "current_level": "High"},
        "Operational Risk": {"probability": 0.8, "impact": 0.9, "current_level": "High"},
        "Market Risk": {"probability": 0.3, "impact": 0.6, "current_level": "Low"},
        "Liquidity Risk": {"probability": 0.2, "impact": 0.7, "current_level": "Low"},
        "Regulatory Risk": {"probability": 0.5, "impact": 0.8, "current_level": "Medium"},
        "Technology Risk": {"probability": 0.4, "impact": 0.7, "current_level": "Medium"},
        "Reputational Risk": {"probability": 0.6, "impact": 0.9, "current_level": "High"}
    }
    
    # Create risk matrix visualization
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        high_risks = [k for k, v in risk_matrix.items() if v["current_level"] == "High"]
        st.error(f"🔴 **High Risk ({len(high_risks)})**")
        for risk in high_risks:
            st.write(f"• {risk}")
    
    with col2:
        medium_risks = [k for k, v in risk_matrix.items() if v["current_level"] == "Medium"]
        st.warning(f"🟡 **Medium Risk ({len(medium_risks)})**")
        for risk in medium_risks:
            st.write(f"• {risk}")
    
    with col3:
        low_risks = [k for k, v in risk_matrix.items() if v["current_level"] == "Low"]
        st.success(f"🟢 **Low Risk ({len(low_risks)})**")
        for risk in low_risks:
            st.write(f"• {risk}")
    
    with col4:
        overall_risk_score = np.mean([v["probability"] * v["impact"] for v in risk_matrix.values()]) * 100
        st.metric("Overall Risk Score", f"{overall_risk_score:.0f}/100", "⚠️ High")
    
    # Detailed Risk Analysis
    st.markdown("## 📊 Detailed Risk Analysis")
    
    for risk_type, risk_data in risk_matrix.items():
        risk_score = risk_data["probability"] * risk_data["impact"] * 100
        
        with st.expander(f"{risk_type} - Score: {risk_score:.0f}/100 ({risk_data['current_level']})"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Probability", f"{risk_data['probability']*100:.0f}%")
                st.progress(risk_data["probability"])
            
            with col2:
                st.metric("Impact", f"{risk_data['impact']*100:.0f}%")
                st.progress(risk_data["impact"])
            
            with col3:
                st.metric("Risk Score", f"{risk_score:.0f}/100")
                st.progress(risk_score/100)
            
            # Risk-specific details
            if risk_type == "Credit Risk":
                st.markdown("**Key Indicators:**")
                st.write("• NPF Gross: 3.99% (trending upward)")
                st.write("• Large exposure concentration")
                st.write("• Economic slowdown impact")
                
                st.markdown("**Mitigation Strategies:**")
                st.write("• Enhanced credit scoring models")
                st.write("• Diversification of portfolio")
                st.write("• Regular stress testing")
            
            elif risk_type == "Operational Risk":
                st.markdown("**Key Indicators:**")
                st.write("• BOPO: 98.5% (well above benchmark)")
                st.write("• Process inefficiencies")
                st.write("• Technology gaps")
                
                st.markdown("**Mitigation Strategies:**")
                st.write("• Process automation")
                st.write("• Staff training programs")
                st.write("• Technology upgrades")
    
    # Risk Appetite and Limits
    st.markdown("## 🎯 Risk Appetite & Limits")
    
    risk_limits = {
        "NPF Ratio": {"current": 3.99, "limit": 5.0, "threshold": 4.0},
        "CAR": {"current": 29.42, "limit": 8.0, "threshold": 12.0},
        "BOPO": {"current": 98.5, "limit": 94.0, "threshold": 90.0},
        "Single Borrower Limit": {"current": 18.5, "limit": 20.0, "threshold": 15.0}
    }
    
    for metric, data in risk_limits.items():
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.write(f"**{metric}**")
        
        with col2:
            st.write(f"Current: {data['current']:.1f}%")
        
        with col3:
            st.write(f"Threshold: {data['threshold']:.1f}%")
        
        with col4:
            if metric in ["NPF Ratio", "BOPO"]:
                # For these metrics, lower is better
                if data["current"] > data["limit"]:
                    st.error("🔴 Breach")
                elif data["current"] > data["threshold"]:
                    st.warning("🟡 Warning")
                else:
                    st.success("🟢 Safe")
            else:
                # For CAR and other metrics, higher is better
                if data["current"] < data["limit"]:
                    st.error("🔴 Breach")
                elif data["current"] < data["threshold"]:
                    st.warning("🟡 Warning")
                else:
                    st.success("🟢 Safe")

# ===== pages/compliance_monitoring.py =====
"""
Compliance Monitoring Module
"""

import streamlit as st
from datetime import datetime, timedelta

def render_compliance_monitoring():
    """Render compliance monitoring dashboard"""
    
    st.title("📋 Compliance Monitoring Dashboard")
    st.markdown("*Regulatory compliance tracking and reporting system*")
    
    # Compliance Overview
    st.markdown("## 📊 Compliance Overview")
    
    compliance_score = 87.5
    open_issues = 5
    closed_issues = 23
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Compliance Score", f"{compliance_score:.1f}%", "📊 Good")
    
    with col2:
        st.metric("Open Issues", open_issues, "🔄 In Progress")
    
    with col3:
        st.metric("Closed Issues", closed_issues, "✅ This Month")
    
    with col4:
        next_audit = datetime.now() + timedelta(days=45)
        st.metric("Next Audit", next_audit.strftime("%b %Y"), "📅 Scheduled")
    
    # Regulatory Requirements Tracking
    st.markdown("## 🎯 Regulatory Requirements")
    
    regulations = {
        "Capital Adequacy (CAR)": {
            "requirement": "Minimum 8%",
            "current": "29.42%",
            "status": "Compliant",
            "last_check": "2024-07-15",
            "next_check": "2024-08-15"
        },
        "Non-Performing Financing (NPF)": {
            "requirement": "Maximum 5%",
            "current": "3.99%",
            "status": "Compliant",
            "last_check": "2024-07-15",
            "next_check": "2024-08-15"
        },
        "Operational Efficiency (BOPO)": {
            "requirement": "Maximum 94%",
            "current": "98.5%",
            "status": "Non-Compliant",
            "last_check": "2024-07-15",
            "next_check": "2024-08-15"
        },
        "Liquidity Coverage Ratio": {
            "requirement": "Minimum 100%",
            "current": "125.5%",
            "status": "Compliant",
            "last_check": "2024-07-15",
            "next_check": "2024-08-15"
        },
        "Islamic Banking Compliance": {
            "requirement": "100% Sharia Compliant",
            "current": "99.8%",
            "status": "Minor Issues",
            "last_check": "2024-07-10",
            "next_check": "2024-08-10"
        }
    }
    
    for reg_name, reg_data in regulations.items():
        with st.expander(f"{reg_name} - {reg_data['status']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Requirement**: {reg_data['requirement']}")
                st.write(f"**Current Value**: {reg_data['current']}")
                
                # Status indicator
                if reg_data['status'] == "Compliant":
                    st.success(f"✅ {reg_data['status']}")
                elif reg_data['status'] == "Non-Compliant":
                    st.error(f"❌ {reg_data['status']}")
                else:
                    st.warning(f"⚠️ {reg_data['status']}")
            
            with col2:
                st.write(f"**Last Check**: {reg_data['last_check']}")
                st.write(f"**Next Check**: {reg_data['next_check']}")
            
            with col3:
                if reg_data['status'] == "Non-Compliant":
                    st.error("**Action Required**")
                    st.write("• Develop improvement plan")
                    st.write("• Set timeline for compliance")
                    st.write("• Regular monitoring")
                elif reg_data['status'] == "Minor Issues":
                    st.warning("**Minor Action Required**")
                    st.write("• Address identified issues")
                    st.write("• Document corrective actions")
                else:
                    st.success("**No Action Required**")
                    st.write("• Continue monitoring")
                    st.write("• Maintain current practices")
    
    # Compliance Issues Tracker
    st.markdown("## 🚨 Active Compliance Issues")
    
    issues = [
        {
            "id": "COMP-001",
            "category": "Operational Efficiency",
            "description": "BOPO ratio exceeds regulatory limit of 94%",
            "severity": "High",
            "opened": "2024-06-15",
            "due_date": "2024-08-15",
            "owner": "Operations Team",
            "status": "In Progress"
        },
        {
            "id": "COMP-002", 
            "category": "Islamic Banking",
            "description": "Minor Sharia compliance gaps in product documentation",
            "severity": "Medium",
            "opened": "2024-07-01",
            "due_date": "2024-08-01",
            "owner": "Sharia Board",
            "status": "In Progress"
        },
        {
            "id": "COMP-003",
            "category": "Reporting",
            "description": "Late submission of monthly regulatory reports",
            "severity": "Low",
            "opened": "2024-07-10",
            "due_date": "2024-07-25",
            "owner": "Compliance Team",
            "status": "Open"
        }
    ]
    
    for issue in issues:
        severity_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}[issue["severity"]]
        
        with st.expander(f"{severity_color} {issue['id']}: {issue['description'][:50]}..."):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**ID**: {issue['id']}")
                st.write(f"**Category**: {issue['category']}")
                st.write(f"**Severity**: {issue['severity']}")
                st.write(f"**Status**: {issue['status']}")
            
            with col2:
                st.write(f"**Opened**: {issue['opened']}")
                st.write(f"**Due Date**: {issue['due_date']}")
                st.write(f"**Owner**: {issue['owner']}")
                
                # Action buttons
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button(f"Update {issue['id']}", key=f"update_{issue['id']}"):
                        st.success(f"Issue {issue['id']} updated!")
                with col_b:
                    if st.button(f"Close {issue['id']}", key=f"close_{issue['id']}"):
                        st.success(f"Issue {issue['id']} closed!")

# ===== pages/strategic_analysis.py =====
"""
Strategic Analysis Module
"""

import streamlit as st

def render_strategic_analysis():
    """Render strategic analysis dashboard"""
    
    st.title("🎯 Strategic Analysis Dashboard")
    st.markdown("*Strategic planning, performance analysis and business intelligence*")
    
    # Strategic Overview
    st.markdown("## 📊 Strategic Performance Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Strategic Score", "68/100", "📊 Developing")
    
    with col2:
        st.metric("Market Position", "#4", "🏦 Islamic Banks ID")
    
    with col3:
        st.metric("Growth Rate", "5.2%", "📈 YoY Assets")
    
    with col4:
        st.metric("Market Share", "2.8%", "🏦 Islamic Banking")
    
    # SWOT Analysis
    st.markdown("## 🎯 SWOT Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💪 **Strengths**")
        strengths = [
            "Strong capital position (CAR 29.42%)",
            "Established Islamic banking expertise",
            "Regulatory compliance track record",
            "Experienced management team",
            "Diverse product portfolio"
        ]
        for strength in strengths:
            st.success(f"✅ {strength}")
        
        st.markdown("### ⚡ **Opportunities**")
        opportunities = [
            "Growing Islamic finance market in Indonesia",
            "Digital banking transformation potential",
            "Strategic partnerships with fintech",
            "Expansion to underserved markets",
            "Corporate banking growth"
        ]
        for opportunity in opportunities:
            st.info(f"🚀 {opportunity}")
    
    with col2:
        st.markdown("### ⚠️ **Weaknesses**")
        weaknesses = [
            "High operational costs (BOPO 98.5%)",
            "Lower profitability vs peers",
            "Asset quality concerns (NPF 3.99%)",
            "Limited digital capabilities",
            "Branch network optimization needed"
        ]
        for weakness in weaknesses:
            st.error(f"❌ {weakness}")
        
        st.markdown("### 🛡️ **Threats**")
        threats = [
            "Intense competition from larger banks",
            "Regulatory changes and compliance costs",
            "Economic slowdown impact",
            "Technology disruption",
            "Customer behavior changes"
        ]
        for threat in threats:
            st.warning(f"⚠️ {threat}")
    
    # Strategic Initiatives
    st.markdown("## 🚀 Strategic Initiatives 2024-2026")
    
    initiatives = [
        {
            "name": "Operational Excellence Program",
            "objective": "Reduce BOPO to below 94%",
            "timeline": "12 months",
            "budget": "Rp 50B",
            "progress": 25,
            "status": "In Progress",
            "owner": "COO"
        },
        {
            "name": "Digital Transformation",
            "objective": "Launch comprehensive digital banking platform",
            "timeline": "18 months", 
            "budget": "Rp 150B",
            "progress": 40,
            "status": "In Progress",
            "owner": "CTO"
        },
        {
            "name": "Asset Quality Enhancement",
            "objective": "Reduce NPF to below 3%",
            "timeline": "24 months",
            "budget": "Rp 25B",
            "progress": 15,
            "status": "Planning",
            "owner": "CRO"
        },
        {
            "name": "Market Expansion",
            "objective": "Increase market share to 4%",
            "timeline": "36 months",
            "budget": "Rp 200B",
            "progress": 10,
            "status": "Planning",
            "owner": "CEO"
        }
    ]
    
    for initiative in initiatives:
        with st.expander(f"{initiative['name']} - {initiative['progress']}% Complete"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Objective**: {initiative['objective']}")
                st.write(f"**Timeline**: {initiative['timeline']}")
                st.write(f"**Owner**: {initiative['owner']}")
            
            with col2:
                st.write(f"**Budget**: {initiative['budget']}")
                st.write(f"**Status**: {initiative['status']}")
                st.progress(initiative['progress'] / 100)
            
            with col3:
                if initiative['status'] == "In Progress":
                    st.success("🟢 Active")
                elif initiative['status'] == "Planning":
                    st.warning("🟡 Planning")
                else:
                    st.info("🔵 Scheduled")

# ===== pages/decision_support.py =====
"""
Decision Support System Module
"""

import streamlit as st

def render_decision_support():
    """Render AI-powered decision support system"""
    
    st.title("🤝 Decision Support System")
    st.markdown("*AI-powered insights, recommendations and decision assistance*")
    
    # Current Decision Priorities
    st.markdown("## 🎯 Priority Decisions")
    
    decisions = [
        {
            "title": "Operational Efficiency Improvement",
            "urgency": "High",
            "impact": "High", 
            "confidence": 95,
            "recommendation": "Implement immediate cost reduction and automation program",
            "rationale": "BOPO at 98.5% significantly impacts profitability and regulatory compliance",
            "options": [
                "Aggressive cost cutting (6 months)",
                "Gradual automation (12 months)", 
                "Hybrid approach (9 months)"
            ],
            "ai_recommendation": "Hybrid approach recommended for optimal risk-reward balance"
        },
        {
            "title": "NPF Management Strategy",
            "urgency": "Medium",
            "impact": "High",
            "confidence": 88,
            "recommendation": "Strengthen credit risk management and collection procedures",
            "rationale": "NPF trending toward regulatory threshold, early intervention needed",
            "options": [
                "Enhanced collection efforts",
                "Portfolio restructuring",
                "Write-off acceleration"
            ],
            "ai_recommendation": "Enhanced collection with selective restructuring"
        },
        {
            "title": "Digital Banking Investment",
            "urgency": "Medium",
            "impact": "Medium",
            "confidence": 75,
            "recommendation": "Proceed with phased digital transformation",
            "rationale": "Market demands digital capabilities for competitive positioning",
            "options": [
                "Full platform overhaul",
                "Gradual feature rollout",
                "Partnership with fintech"
            ],
            "ai_recommendation": "Gradual rollout with selective partnerships"
        }
    ]
    
    for i, decision in enumerate(decisions, 1):
        urgency_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}[decision["urgency"]]
        impact_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}[decision["impact"]]
        
        with st.expander(f"{i}. {decision['title']} {urgency_color} {impact_color}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Urgency**: {decision['urgency']}")
                st.write(f"**Impact**: {decision['impact']}")
                st.write(f"**AI Confidence**: {decision['confidence']}%")
                st.progress(decision['confidence'] / 100)
                
                st.write(f"**Rationale**: {decision['rationale']}")
            
            with col2:
                st.write(f"**AI Recommendation**: {decision['recommendation']}")
                
                st.write("**Available Options**:")
                for option in decision['options']:
                    st.write(f"• {option}")
                
                st.success(f"**Best Choice**: {decision['ai_recommendation']}")
                
                # Action buttons
                if st.button(f"Accept Recommendation {i}", key=f"accept_{i}"):
                    st.success(f"✅ Recommendation {i} accepted and added to action plan")
                
                if st.button(f"Request More Analysis {i}", key=f"analyze_{i}"):
                    st.info(f"🔍 Additional analysis requested for decision {i}")
    
    # AI Insights
    st.markdown("## 💡 AI-Generated Insights")
    
    insights = [
        {
            "category": "Performance",
            "insight": "Bank's operational efficiency is the primary constraint on profitability growth",
            "confidence": 92,
            "data_source": "5-year operational data analysis"
        },
        {
            "category": "Risk",
            "insight": "Asset quality shows early warning signs requiring proactive management",
            "confidence": 87,
            "data_source": "Credit risk modeling and peer comparison"
        },
        {
            "category": "Market",
            "insight": "Digital banking adoption accelerating, creating competitive pressure",
            "confidence": 83,
            "data_source": "Market research and customer behavior analysis"
        },
        {
            "category": "Regulatory",
            "insight": "Regulatory focus shifting toward operational efficiency metrics",
            "confidence": 78,
            "data_source": "Regulatory trend analysis"
        }
    ]
    
    for insight in insights:
        confidence_color = "🟢" if insight['confidence'] >= 85 else "🟡" if insight['confidence'] >= 70 else "🔴"
        
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.info(f"**{insight['category']}**: {insight['insight']}")
            
            with col2:
                st.write(f"{confidence_color} {insight['confidence']}%")
            
            with col3:
                st.caption(insight['data_source'])

# ===== pages/app_info.py =====
"""
Application Information Module
"""

import streamlit as st

def render_app_info():
    """Render application information and documentation"""
    
    st.title("ℹ️ Bank Muamalat Health Monitor")
    st.markdown("*Application Information, Documentation and System Status*")
    
    # Application Overview
    st.markdown("## 🏦 Application Overview")
    
    st.markdown("""
    **Bank Muamalat Health Monitor** is a comprehensive financial monitoring and analysis 
    system designed specifically for Bank Muamalat Indonesia. The application provides 
    real-time insights into financial performance, risk assessment, compliance monitoring, 
    and strategic decision support.
    """)
    
    # Feature Matrix
    st.markdown("## ✨ Feature Matrix")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 **Core Modules**")
        features = [
            ("Dashboard Overview", "✅", "Real-time financial metrics display"),
            ("Auto Data Scraper", "✅", "Automated data collection system"),
            ("Financial Health", "✅", "Comprehensive health assessment"),
            ("Risk Assessment", "✅", "Multi-dimensional risk analysis"),
            ("Compliance Monitoring", "✅", "Regulatory compliance tracking"),
            ("Strategic Analysis", "✅", "SWOT and strategic planning"),
            ("Decision Support", "✅", "AI-powered recommendations")
        ]
        
        for feature, status, description in features:
            st.write(f"{status} **{feature}**")
            st.caption(description)
    
    with col2:
        st.markdown("### 🛠️ **Technical Features**")
        tech_features = [
            ("Multi-page Architecture", "✅", "Modular page system"),
            ("Fallback System", "✅", "Graceful degradation"),
            ("Interactive Charts", "✅", "Plotly visualizations"),
            ("Data Export", "✅", "CSV, JSON, Excel formats"),
            ("Session Management", "✅", "Stateful user experience"),
            ("Error Handling", "✅", "Robust error management"),
            ("Responsive Design", "✅", "Mobile-friendly interface")
        ]
        
        for feature, status, description in tech_features:
            st.write(f"{status} **{feature}**")
            st.caption(description)
    
    # Technical Specifications
    st.markdown("## 🔧 Technical Specifications")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### **Frontend**")
        st.write("• **Framework**: Streamlit")
        st.write("• **Styling**: Custom CSS")
        st.write("• **Charts**: Plotly")
        st.write("• **Icons**: Unicode/Emoji")
    
    with col2:
        st.markdown("### **Backend**")
        st.write("• **Language**: Python 3.8+")
        st.write("• **Data Processing**: Pandas")
        st.write("• **Web Scraping**: BeautifulSoup")
        st.write("• **HTTP**: Requests")
    
    with col3:
        st.markdown("### **Deployment**")
        st.write("• **Local**: Streamlit run")
        st.write("• **Cloud**: Streamlit Cloud")
        st.write("• **Storage**: Session-based")
        st.write("• **Config**: TOML files")
    
    # System Status
    st.markdown("## 📊 System Status")
    
    # Check module availability
    modules_status = {
        "streamlit": True,
        "pandas": True,
        "plotly": True,
        "requests": False,  # Would be determined dynamically
        "beautifulsoup4": False  # Would be determined dynamically
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### **Core Dependencies**")
        for module, available in modules_status.items():
            if available:
                st.success(f"✅ {module}")
            else:
                st.warning(f"⚠️ {module} (Optional)")
    
    with col2:
        st.markdown("### **System Health**")
        total_modules = len(modules_status)
        available_modules = sum(modules_status.values())
        health_percentage = (available_modules / total_modules) * 100
        
        st.metric("Health Score", f"{health_percentage:.0f}%")
        st.metric("Available Modules", f"{available_modules}/{total_modules}")
        
        if health_percentage >= 80:
            st.success("🟢 System Healthy")
        elif health_percentage >= 60:
            st.warning("🟡 Partial Functionality")
        else:
            st.error("🔴 Limited Functionality")
    
    # Installation Guide
    st.markdown("## 📦 Installation Guide")
    
    with st.expander("🚀 Quick Start Installation"):
        st.markdown("""
        ### **Step 1: Clone or Download**
        ```bash
        # Download the application files
        # Ensure you have the complete directory structure
        ```
        
        ### **Step 2: Install Dependencies**
        ```bash
        # Minimum installation
        pip install streamlit pandas
        
        # Full installation (recommended)
        pip install streamlit pandas plotly requests beautifulsoup4
        ```
        
        ### **Step 3: Run Application**
        ```bash
        # Run with multi-page support
        streamlit run app/main.py
        
        # Or run individual modules
        streamlit run auto_scraper.py
        ```
        
        ### **Step 4: Access Application**
        ```
        Open browser and navigate to:
        http://localhost:8501
        ```
        """)
    
    # Support Information
    st.markdown("## 🆘 Support & Documentation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### **Getting Help**")
        st.write("• Check the troubleshooting guide")
        st.write("• Review system requirements")
        st.write("• Verify file structure")
        st.write("• Check dependency installation")
    
    with col2:
        st.markdown("### **Version Information**")
        st.write("• **Version**: 2.0.0 Enhanced")
        st.write("• **Release**: July 2024")
        st.write("• **Compatibility**: Python 3.8+")
        st.write("• **License**: Open Source")
    
    # Footer
    st.markdown("---")
    st.markdown("### 💼 **About Bank Muamalat Indonesia**")
    st.info("""
    Bank Muamalat Indonesia is the first Islamic bank in Indonesia, established in 1991. 
    As a pioneer in Islamic banking, the bank is committed to providing Sharia-compliant 
    financial services while maintaining high standards of performance and compliance.
    """)