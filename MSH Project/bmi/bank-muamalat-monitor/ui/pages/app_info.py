"""
Application Information Page
"""

import streamlit as st
import sys
from datetime import datetime
from typing import Optional, Any

def render(orchestrator: Optional[Any] = None):
    """Render the application information page"""
    
    # Import config safely
    try:
        from app.config import config
    except ImportError:
        st.error("Configuration not available")
        return
    
    st.title("ℹ️ Application Information")
    st.markdown("### System Details & Build Information")
    
    # Application Info
    app_info = config.get_app_info()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📱 Application Details")
        st.info(f"""
        **Name:** {app_info['name']}  
        **Version:** {app_info['version']}  
        **Build Date:** {app_info['build_date']}  
        **Developer:** {app_info['developer']}  
        **Organization:** {app_info['organization']}
        """)
        
        st.markdown("#### 🔧 Technical Stack")
        st.info(f"""
        **Framework:** Streamlit  
        **Language:** Python {sys.version.split()[0]}  
        **AI Engine:** RAG-based Decision Support  
        **Visualization:** Plotly  
        **Data Processing:** Pandas, NumPy
        """)
    
    with col2:
        st.markdown("#### 🏢 Organization")
        st.info("""
        **BPKH**  
        (Badan Pengelola Keuangan Haji)
        
        **Purpose:** Strategic monitoring and decision support 
        for Bank Muamalat Indonesia investment analysis
        
        **Target Users:** BPKH Board Members, Investment Committee, 
        Risk Management Team
        """)
        
        st.markdown("#### 📊 Data Sources")
        st.info("""
        **Primary Sources:**
        - OJK (Otoritas Jasa Keuangan)
        - Bank Indonesia
        - Bank Muamalat Annual Reports
        - Bloomberg/Reuters (Market Data)
        
        **Update Frequency:** Real-time & Daily
        """)
    
    # Feature Overview
    st.markdown("### 🎯 Feature Overview")
    
    features = [
        {"name": "Overview Dashboard", "description": "Real-time KPI monitoring and health score", "status": "✅ Active"},
        {"name": "Financial Health", "description": "Comprehensive financial performance analysis", "status": "✅ Active"},
        {"name": "Risk Assessment", "description": "Multi-dimensional risk monitoring", "status": "✅ Active"},
        {"name": "Compliance & GRC", "description": "Governance, Risk, and Compliance oversight", "status": "✅ Active"},
        {"name": "Strategic Analysis", "description": "Strategic positioning and market analysis", "status": "✅ Active"},
        {"name": "Decision Support", "description": "AI-powered recommendations and scenarios", "status": "✅ Active"},
        {"name": "AI Orchestrator", "description": "Advanced AI agents for deep analysis", "status": "🔄 Development"},
        {"name": "Real-time Alerts", "description": "Automated threshold-based notifications", "status": "🔄 Development"}
    ]
    
    for feature in features:
        col1, col2, col3 = st.columns([2, 4, 1])
        with col1:
            st.write(f"**{feature['name']}**")
        with col2:
            st.write(feature['description'])
        with col3:
            st.write(feature['status'])
    
    # Version History
    st.markdown("### 📋 Version History")
    
    with st.expander("View Version History"):
        st.markdown("""
        **Version 2024.07.17-build1430** (Current)
        - ✅ Complete dashboard implementation
        - ✅ All 6 main pages functional
        - ✅ Dynamic versioning system
        - ✅ Enhanced footer with disclaimer
        - ✅ Developer information integration
        
        **Version 2024.07.16-build0900**
        - ✅ Core dashboard structure
        - ✅ Basic metric cards
        - ✅ Plotly integration
        - ✅ Safe import system
        
        **Version 2024.07.15-build1600**
        - ✅ Project initialization
        - ✅ Streamlit setup
        - ✅ Basic page routing
        - ✅ Configuration system
        """)
    
    # System Status
    st.markdown("### 🔍 System Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("System Status", "🟢 Online", "")
        st.metric("Pages", "6/6", "All Active")
    
    with col2:
        st.metric("Data Freshness", "Real-time", "")
        st.metric("AI Agents", "Ready", "")
    
    with col3:
        st.metric("Response Time", "< 2s", "")
        st.metric("Uptime", "99.9%", "")
    
    # Debug Information (if debug mode)
    if config.DEBUG:
        st.markdown("### 🐛 Debug Information")
        
        with st.expander("Debug Details"):
            st.json({
                "session_state": dict(st.session_state),
                "config": config.get_build_info(),
                "python_version": sys.version,
                "streamlit_version": st.__version__,
                "current_time": datetime.now().isoformat()
            })
    
    # Contact Information
    st.markdown("### 📞 Contact & Support")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Developer Contact:**
        - **Name:** MS Hadianto
        - **Position:** Komite Audit
        - **Organization:** BPKH
        - **Email:** sopian@bpkh.go.id
        """)
    
    with col2:
        st.markdown("""
        **Technical Support:**
        - **Issues:** Create ticket via internal system
        - **Feature Requests:** Contact development team
        - **Training:** Available upon request
        - **Documentation:** Available in system help
        """)

# Export the render function
__all__ = ['render']