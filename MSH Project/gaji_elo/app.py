"""
Salary Estimator RAG Application
Built with Streamlit, RAG, and Agentic AI
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import tempfile
import logging
from datetime import datetime
from typing import Dict, Any

from src.cv_parser import CVParser
from src.salary_matcher import SalaryMatcher
from models.schemas import CVProfile, SalaryEstimation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="AI Salary Estimator - Indonesia 2025",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1e3d59;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #3e5c76;
        text-align: center;
        margin-bottom: 3rem;
    }
    .metric-card {
        background-color: #f5f5f5;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .recommendation-card {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #1e3d59;
    }
    .stButton>button {
        background-color: #1e3d59;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cv_profile' not in st.session_state:
    st.session_state.cv_profile = None
if 'salary_estimation' not in st.session_state:
    st.session_state.salary_estimation = None


def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🤖 AI-Powered Salary Estimator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Based on Indonesia Salary Guide 2025 | Powered by RAG & Agentic AI</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📋 About This Tool")
        st.info(
            "This AI-powered tool analyzes your CV and provides accurate salary estimations "
            "based on the official Indonesia Salary Guide 2025.\n\n"
            "**Features:**\n"
            "- 🔍 Smart CV parsing\n"
            "- 🎯 Industry-specific matching\n"
            "- 📊 Data-driven insights\n"
            "- 💡 Career recommendations"
        )
        
        st.header("🔧 How It Works")
        st.markdown(
            "1. **Upload** your CV (PDF format)\n"
            "2. **AI analyzes** your profile\n"
            "3. **RAG searches** salary database\n"
            "4. **Get insights** and recommendations"
        )
        
        # Add reference to team
        st.markdown("---")
        st.caption("Built by MS Hadianto | RAG & Agentic AI Enthusiast")
        
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📄 Upload Your CV")
        
        uploaded_file = st.file_uploader(
            "Choose your CV file (LinkedIn format preferred)",
            type=['pdf'],
            help="Upload your CV in PDF format. LinkedIn CV exports work best!"
        )
        
        if uploaded_file is not None:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
                
            # Parse CV button
            if st.button("🚀 Analyze My CV", type="primary", use_container_width=True):
                with st.spinner("🔍 Parsing your CV..."):
                    try:
                        # Parse CV
                        parser = CVParser()
                        cv_profile = parser.parse_cv(tmp_file_path)
                        st.session_state.cv_profile = cv_profile
                        
                        # Show success
                        st.success("✅ CV parsed successfully!")
                        
                    except Exception as e:
                        st.error(f"❌ Error parsing CV: {str(e)}")
                        logger.error(f"CV parsing error: {str(e)}")
                        
    with col2:
        st.header("📈 Quick Stats")
        
        if st.session_state.cv_profile:
            profile = st.session_state.cv_profile
            
            # Display profile summary
            st.metric("Current Title", profile.current_title or "Not specified")
            st.metric("Experience Level", profile.experience_level.value.title())
            st.metric("Total Experience", f"{profile.total_experience_years:.1f} years")
            st.metric("Industry", profile.detected_industry.value if profile.detected_industry else "Not detected")
            
    # Show CV details if parsed
    if st.session_state.cv_profile:
        st.markdown("---")
        
        # Profile details in expandable section
        with st.expander("👤 Profile Details", expanded=False):
            profile = st.session_state.cv_profile
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("📧 Contact")
                st.write(f"**Email:** {profile.email or 'Not found'}")
                st.write(f"**Phone:** {profile.phone or 'Not found'}")
                st.write(f"**Location:** {profile.location or 'Not specified'}")
                
            with col2:
                st.subheader("🎓 Education")
                st.write(f"**Level:** {profile.education_level.value.replace('_', ' ').title()}")
                if profile.education_details:
                    for edu in profile.education_details[:2]:
                        st.write(f"- {edu.get('details', '')}")
                        
            with col3:
                st.subheader("💼 Skills")
                st.write(f"**Technical:** {len(profile.technical_skills)} skills")
                st.write(f"**Soft Skills:** {len(profile.soft_skills)} skills")
                st.write(f"**Certifications:** {len(profile.certifications)}")
                
        # Estimate Salary button
        st.markdown("---")
        
        if st.button("💰 Estimate My Salary", type="primary", use_container_width=True):
            with st.spinner("🤖 AI is analyzing salary data..."):
                try:
                    # Estimate salary
                    matcher = SalaryMatcher()
                    salary_estimation = matcher.estimate_salary(st.session_state.cv_profile)
                    st.session_state.salary_estimation = salary_estimation
                    
                    st.success("✅ Salary estimation complete!")
                    
                except Exception as e:
                    st.error(f"❌ Error estimating salary: {str(e)}")
                    logger.error(f"Salary estimation error: {str(e)}")
                    
    # Show salary estimation results
    if st.session_state.salary_estimation:
        show_salary_results(st.session_state.salary_estimation, st.session_state.cv_profile)


def show_salary_results(estimation: SalaryEstimation, profile: CVProfile):
    """Display salary estimation results."""
    
    st.markdown("---")
    st.header("💰 Your Salary Estimation Results")
    
    # Main salary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "Minimum Salary",
            f"IDR {estimation.estimated_salary_min}M",
            f"Monthly"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "Average Salary",
            f"IDR {estimation.estimated_salary_avg}M",
            f"Monthly",
            delta_color="normal"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "Maximum Salary",
            f"IDR {estimation.estimated_salary_max}M",
            f"Monthly"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "Match Confidence",
            f"{estimation.match_confidence * 100:.0f}%",
            "AI Confidence"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Salary range visualization
    st.subheader("📊 Salary Range Visualization")
    
    fig = go.Figure()
    
    # Add salary range
    fig.add_trace(go.Box(
        y=[estimation.estimated_salary_min, 
           estimation.estimated_salary_avg, 
           estimation.estimated_salary_max],
        name="Your Estimated Range",
        boxpoints='all',
        jitter=0.3,
        pointpos=-1.8,
        marker_color='rgb(30, 61, 89)'
    ))
    
    # Add matched positions for comparison
    if estimation.matched_positions:
        matched_salaries = [p['salary'] for p in estimation.matched_positions[:5]]
        fig.add_trace(go.Box(
            y=matched_salaries,
            name="Similar Positions",
            boxpoints='all',
            jitter=0.3,
            pointpos=-1.8,
            marker_color='rgb(62, 92, 118)'
        ))
        
    fig.update_layout(
        title="Salary Distribution Analysis",
        yaxis_title="Monthly Salary (IDR Millions)",
        showlegend=True,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Two columns for additional insights
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Matched positions
        st.subheader("🎯 Best Matching Positions")
        
        if estimation.matched_positions:
            matched_df = pd.DataFrame(estimation.matched_positions[:5])
            matched_df['match_score'] = matched_df['match_score'].apply(lambda x: f"{x*100:.0f}%")
            matched_df = matched_df[['title', 'industry', 'salary', 'match_score']]
            matched_df.columns = ['Position', 'Industry', 'Salary (IDR M)', 'Match %']
            
            st.dataframe(matched_df, use_container_width=True, hide_index=True)
            
    with col2:
        # Salary factors
        st.subheader("📈 Salary Calculation Factors")
        
        factors_df = pd.DataFrame({
            'Factor': ['Experience', 'Education', 'Skills', 'Location'],
            'Multiplier': [
                f"{estimation.experience_factor:.2f}x",
                f"{estimation.education_factor:.2f}x",
                f"{estimation.skills_factor:.2f}x",
                f"{estimation.location_factor:.2f}x"
            ],
            'Impact': [
                _get_impact_label(estimation.experience_factor),
                _get_impact_label(estimation.education_factor),
                _get_impact_label(estimation.skills_factor),
                _get_impact_label(estimation.location_factor)
            ]
        })
        
        st.dataframe(factors_df, use_container_width=True, hide_index=True)
        
    # AI Analysis
    if estimation.explanation:
        st.subheader("🤖 AI Analysis")
        st.info(estimation.explanation)
        
    # Recommendations
    if estimation.recommendations:
        st.subheader("💡 Career Advancement Recommendations")
        
        for idx, rec in enumerate(estimation.recommendations, 1):
            st.markdown(
                f'<div class="recommendation-card">'
                f'<strong>{idx}.</strong> {rec}'
                f'</div>',
                unsafe_allow_html=True
            )
            
    # Additional insights
    st.subheader("📊 Market Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Create experience level comparison
        exp_data = {
            'Experience Level': ['Entry', 'Junior', 'Mid', 'Senior', 'Expert'],
            'Avg Salary': [15, 27, 47, 80, 150]
        }
        exp_df = pd.DataFrame(exp_data)
        
        fig_exp = px.bar(
            exp_df, 
            x='Experience Level', 
            y='Avg Salary',
            title='Average Salary by Experience Level',
            color='Avg Salary',
            color_continuous_scale='Blues'
        )
        fig_exp.update_layout(showlegend=False)
        st.plotly_chart(fig_exp, use_container_width=True)
        
    with col2:
        # Industry comparison (if available)
        if estimation.matched_positions:
            industries = {}
            for pos in estimation.matched_positions:
                ind = pos.get('industry', 'Unknown')
                if ind not in industries:
                    industries[ind] = []
                industries[ind].append(pos['salary'])
                
            ind_avg = {k: sum(v)/len(v) for k, v in industries.items()}
            
            if ind_avg:
                fig_ind = px.pie(
                    values=list(ind_avg.values()),
                    names=list(ind_avg.keys()),
                    title='Salary Distribution by Industry'
                )
                st.plotly_chart(fig_ind, use_container_width=True)
                
    # Export options
    st.markdown("---")
    st.subheader("📥 Export Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Download Report (PDF)", use_container_width=True):
            st.info("PDF export coming soon!")
            
    with col2:
        if st.button("📊 Download Data (Excel)", use_container_width=True):
            st.info("Excel export coming soon!")
            
    with col3:
        if st.button("🔄 Analyze Another CV", use_container_width=True):
            st.session_state.cv_profile = None
            st.session_state.salary_estimation = None
            st.rerun()


def _get_impact_label(factor: float) -> str:
    """Get impact label for a factor."""
    if factor >= 1.15:
        return "⬆️ High"
    elif factor >= 1.05:
        return "↗️ Positive"
    elif factor >= 0.95:
        return "➡️ Neutral"
    elif factor >= 0.85:
        return "↘️ Negative"
    else:
        return "⬇️ Low"


if __name__ == "__main__":
    main()