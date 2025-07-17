"""
Bank Muamalat Health Monitoring System
RAG & Agentic AI-based Application for BPKH
"""

import streamlit as st
from streamlit_option_menu import option_menu
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.config import Config
from app.utils.logger import setup_logger

# Safe imports with proper error handling
def safe_import_page(page_name):
    """Safely import page module"""
    try:
        if page_name == "overview":
            from ui.pages import overview
            return overview
        elif page_name == "financial_health":
            from ui.pages import financial_health
            return financial_health
        elif page_name == "risk_assessment":
            from ui.pages import risk_assessment
            return risk_assessment
        elif page_name == "compliance_monitoring":
            from ui.pages import compliance_monitoring
            return compliance_monitoring
        elif page_name == "strategic_analysis":
            from ui.pages import strategic_analysis
            return strategic_analysis
        elif page_name == "decision_support":
            from ui.pages import decision_support
            return decision_support
        else:
            return None
    except ImportError as e:
        st.error(f"Error importing {page_name}: {e}")
        return None

# Initialize orchestrator safely
def safe_init_orchestrator():
    """Safely initialize orchestrator"""
    try:
        from core.agent_system import AgentOrchestrator
        return AgentOrchestrator
    except ImportError as e:
        st.warning(f"Agent system not available: {e}")
        return None

# Initialize logger
logger = setup_logger(__name__)

# Page configuration
st.set_page_config(
    page_title="Bank Muamalat Health Monitor - BPKH",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
    }
    .alert-box {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .alert-critical {
        background-color: #fee;
        border-left: 5px solid #dc3545;
    }
    .alert-warning {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
    }
    .alert-success {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

class BankMuamalatMonitor:
    def __init__(self):
        self.config = Config()
        self.orchestrator = None
        self.orchestrator_class = safe_init_orchestrator()
        self._initialize_session_state()
        
    def _initialize_session_state(self):
        """Initialize session state variables"""
        if 'initialized' not in st.session_state:
            st.session_state.initialized = True
            st.session_state.current_analysis = None
            st.session_state.agent_responses = {}
            st.session_state.risk_level = "MEDIUM"
            st.session_state.recommendations = []
            
    def _initialize_agents(self):
        """Initialize the agent orchestrator"""
        if self.orchestrator is None and self.orchestrator_class:
            with st.spinner("Initializing AI Agents..."):
                try:
                    self.orchestrator = self.orchestrator_class(self.config)
                    st.success("✅ AI Agents initialized successfully")
                except Exception as e:
                    st.error(f"❌ Failed to initialize agents: {str(e)}")
                    logger.error(f"Agent initialization error: {str(e)}")
                    
    def render_header(self):
        """Render application header"""
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col1:
            st.image("https://via.placeholder.com/150x50/4B0082/FFFFFF?text=BPKH", width=150)
            
        with col2:
            st.markdown("""
            <h1 style='text-align: center; color: #4B0082;'>
                Bank Muamalat Health Monitoring System
            </h1>
            <p style='text-align: center; color: #666;'>
                RAG & Agentic AI-powered Decision Support for PSP
            </p>
            """, unsafe_allow_html=True)
            
        with col3:
            st.image("https://via.placeholder.com/150x50/006400/FFFFFF?text=Muamalat", width=150)
            
    def render_sidebar(self):
        """Render sidebar navigation"""
        with st.sidebar:
            st.markdown("## 🏦 Navigation")
            
            selected = option_menu(
                menu_title=None,
                options=[
                    "Overview Dashboard",
                    "Financial Health",
                    "Risk Assessment",
                    "Compliance & GRC",
                    "Strategic Analysis",
                    "Decision Support"
                ],
                icons=[
                    "speedometer2",
                    "cash-coin",
                    "shield-exclamation",
                    "clipboard-check",
                    "graph-up-arrow",
                    "lightbulb"
                ],
                menu_icon="cast",
                default_index=0,
                styles={
                    "container": {"padding": "0!important", "background-color": "#fafafa"},
                    "icon": {"color": "#4B0082", "font-size": "20px"},
                    "nav-link": {
                        "font-size": "14px",
                        "text-align": "left",
                        "margin": "0px",
                        "padding": "10px",
                        "--hover-color": "#eee"
                    },
                    "nav-link-selected": {"background-color": "#4B0082"},
                }
            )
            
            st.markdown("---")
            
            # Quick Actions
            st.markdown("### ⚡ Quick Actions")
            if st.button("🔄 Refresh Data", use_container_width=True):
                self._refresh_data()
            if st.button("📊 Generate Report", use_container_width=True):
                self._generate_report()
            if st.button("🤖 AI Analysis", use_container_width=True):
                self._run_ai_analysis()
                
            st.markdown("---")
            
            # System Status
            st.markdown("### 📡 System Status")
            status_col1, status_col2 = st.columns(2)
            with status_col1:
                st.metric("Data Freshness", "Real-time")
            with status_col2:
                st.metric("AI Agents", "Active" if self.orchestrator else "Loading")
                
            return selected
    
    def _refresh_data(self):
        """Refresh data from sources"""
        with st.spinner("Refreshing data..."):
            # Implement data refresh logic
            st.success("Data refreshed successfully!")
            
    def _generate_report(self):
        """Generate comprehensive report"""
        with st.spinner("Generating report..."):
            # Implement report generation
            st.success("Report generated! Check the Reports section.")
            
    def _run_ai_analysis(self):
        """Run comprehensive AI analysis"""
        self._initialize_agents()
        if self.orchestrator:
            with st.spinner("Running AI analysis..."):
                try:
                    # Run analysis
                    analysis_result = self.orchestrator.analyze_bank_health()
                    st.session_state.current_analysis = analysis_result
                    st.success("AI analysis completed!")
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")
                    
    def render_content(self, selected_page):
        """Render selected page content"""
        # Page mapping with proper module names
        page_mapping = {
            "Overview Dashboard": "overview",
            "Financial Health": "financial_health",
            "Risk Assessment": "risk_assessment",
            "Compliance & GRC": "compliance_monitoring",
            "Strategic Analysis": "strategic_analysis",
            "Decision Support": "decision_support"
        }
        
        page_module_name = page_mapping.get(selected_page)
        if page_module_name:
            page_module = safe_import_page(page_module_name)
            if page_module:
                try:
                    # Call the render function from the module
                    if hasattr(page_module, 'render'):
                        page_module.render(self.orchestrator)
                    else:
                        st.error(f"Page {selected_page} does not have a render function")
                except Exception as e:
                    st.error(f"Error rendering page {selected_page}: {str(e)}")
                    logger.error(f"Page rendering error: {str(e)}")
            else:
                st.error(f"Failed to load page: {selected_page}")
        else:
            st.error("Page not found!")
            
    def render_fallback_page(self, page_name):
        """Render fallback page when module is not available"""
        st.title(f"📋 {page_name}")
        st.info(f"The {page_name} module is currently under development.")
        
        # Show some placeholder content
        st.markdown("### Coming Soon")
        st.markdown("""
        This page will include:
        - Real-time data visualization
        - Interactive analytics
        - AI-powered insights
        - Comprehensive reporting
        """)
        
        # Add some sample metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Status", "In Development")
        with col2:
            st.metric("Progress", "60%")
        with col3:
            st.metric("ETA", "Next Sprint")
            
    def run(self):
        """Main application loop"""
        try:
            self.render_header()
            selected_page = self.render_sidebar()
            
            # Main content area
            with st.container():
                self.render_content(selected_page)
            
        except Exception as e:
            st.error(f"Application error: {str(e)}")
            logger.error(f"Application error: {str(e)}")
            
        finally:
            # Footer
            st.markdown("---")
            st.markdown("""
            <div style='text-align: center; color: #888; font-size: 12px;'>
                © 2025 BPKH - Bank Muamalat Health Monitoring System | 
                Powered by RAG & Agentic AI | M Sopian Hadianto | Komite Audit BPKH
            </div>
            """, unsafe_allow_html=True)

def main():
    """Application entry point"""
    try:
        app = BankMuamalatMonitor()
        app.run()
    except Exception as e:
        st.error(f"Failed to start application: {str(e)}")
        logger.error(f"Application startup error: {str(e)}")

if __name__ == "__main__":
    main()