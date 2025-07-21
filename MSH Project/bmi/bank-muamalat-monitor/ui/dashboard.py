"""
Updated Dashboard.py - Enhanced with Real-Time Capabilities
Integrated with main.py real-time system
"""

import streamlit as st
from typing import Dict, Any, Optional
import pandas as pd
from datetime import datetime, timedelta
import time

# Try to import plotly for advanced charts
try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

class RealTimeDashboard:
    """
    Enhanced Dashboard class with real-time capabilities
    Integrates with main.py live data system
    """
    
    def __init__(self, config):
        self.config = config
        self.initialize_layout()
        
    def initialize_layout(self):
        """Initialize dashboard layout with real-time features"""
        st.set_page_config(
            page_title="Bank Muamalat Real-Time Dashboard",
            page_icon="🏦",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Enhanced CSS with real-time indicators
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
            position: relative;
        }
        .metric-container:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        .live-indicator {
            position: absolute;
            top: 10px;
            right: 10px;
            background: #dc3545;
            color: white;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.7rem;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
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
        .realtime-status {
            background: linear-gradient(90deg, #28a745, #20c997);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            display: inline-block;
            margin-bottom: 1rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
    def render(self, data: Optional[Dict[str, Any]] = None):
        """Render the real-time dashboard"""
        # Header with real-time status
        self.render_realtime_header()
        
        # Real-time controls
        self.render_realtime_controls()
        
        # Key Metrics with live updates
        self.render_realtime_metrics(data)
        
        # Alerts with time stamps
        self.render_realtime_alerts(data)
        
        # Main content area with live charts
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self.render_realtime_charts(data)
            self.render_trend_analysis(data)
            
        with col2:
            self.render_realtime_risk_dashboard(data)
            self.render_live_insights(data)
            
        # Footer with system status
        self.render_realtime_footer()
        
    def render_realtime_header(self):
        """Render header with real-time clock and status"""
        current_time = datetime.now()
        
        st.markdown(f"""
        <div class="dashboard-header">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1 style='margin: 0;'>🏦 Bank Muamalat Real-Time Dashboard</h1>
                    <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>
                        Live Monitoring & Advanced Analytics
                    </p>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1.5rem; font-weight: bold;">
                        {current_time.strftime('%H:%M:%S')}
                    </div>
                    <div style="opacity: 0.8;">
                        {current_time.strftime('%Y-%m-%d')}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    def render_realtime_controls(self):
        """Render real-time control panel"""
        st.markdown('<div class="realtime-status">🔴 LIVE MODE ACTIVE</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            auto_refresh = st.checkbox("🔄 Auto Refresh", value=True, key="rt_auto_refresh")
            
        with col2:
            refresh_rate = st.selectbox("Refresh Rate", [10, 30, 60, 120], index=1, key="rt_refresh_rate")
            
        with col3:
            period = st.selectbox("Time Period", ["Live", "1H", "24H", "7D"], key="rt_period")
            
        with col4:
            if st.button("🔄 Refresh Now", key="rt_manual_refresh"):
                self._generate_new_data_point()
                st.success("✅ Data refreshed!")
                st.rerun()
                
        with col5:
            if st.button("📊 Export Data", key="rt_export"):
                self._export_realtime_data()
        
        # Auto refresh functionality
        if auto_refresh:
            if 'last_refresh' not in st.session_state:
                st.session_state.last_refresh = time.time()
            
            current_time = time.time()
            if current_time - st.session_state.last_refresh > refresh_rate:
                self._generate_new_data_point()
                st.session_state.last_refresh = current_time
                st.rerun()
            
            # Show countdown
            next_refresh = refresh_rate - int(current_time - st.session_state.last_refresh)
            st.info(f"⏱️ Next auto refresh in: {next_refresh}s")
        
    def render_realtime_metrics(self, data: Optional[Dict[str, Any]]):
        """Render metrics with real-time updates and timestamps"""
        st.markdown("### 📊 Real-Time Key Performance Indicators")
        
        # Get real-time data
        if not data:
            data = self._get_realtime_mock_data()
            
        metrics = data.get('metrics', {})
        timestamp = data.get('timestamp', datetime.now())
        
        # Create metric columns with live indicators
        cols = st.columns(6)
        
        metrics_config = [
            ("CAR", metrics.get('car', 29.42), metrics.get('car_delta', 2.5), "green", "Capital Adequacy Ratio"),
            ("NPF", metrics.get('npf', 3.99), metrics.get('npf_delta', 0.5), "red", "Non-Performing Financing"),
            ("ROA", metrics.get('roa', 0.03), metrics.get('roa_delta', -0.02), "red", "Return on Assets"),
            ("ROE", metrics.get('roe', 0.4), metrics.get('roe_delta', -0.1), "red", "Return on Equity"),
            ("BOPO", metrics.get('bopo', 98.5), metrics.get('bopo_delta', 1.2), "red", "Operating Efficiency"),
            ("FDR", metrics.get('fdr', 85.0), metrics.get('fdr_delta', -2.3), "green", "Financing to Deposit")
        ]
        
        for i, (label, value, delta, status, tooltip) in enumerate(metrics_config):
            with cols[i]:
                self.render_realtime_metric_card(label, value, delta, status, tooltip, timestamp)
                
    def render_realtime_metric_card(self, label: str, value: float, delta: float, status: str, tooltip: str, timestamp: datetime):
        """Render metric card with real-time indicator and timestamp"""
        color_map = {
            'green': '#28a745',
            'yellow': '#ffc107',
            'red': '#dc3545'
        }
        
        # Format value based on metric type
        if label in ['CAR', 'NPF', 'BOPO', 'FDR']:
            display_value = f"{value:.1f}%"
        else:
            display_value = f"{value:.2f}%"
        
        # Format delta
        delta_sign = "+" if delta >= 0 else ""
        delta_color = color_map.get(status, '#6c757d')
        
        # Time since update
        time_ago = datetime.now() - timestamp
        seconds_ago = int(time_ago.total_seconds())
        time_display = f"{seconds_ago}s ago" if seconds_ago < 60 else f"{seconds_ago//60}m ago"
        
        st.markdown(f"""
        <div class="metric-container" style="border-top: 3px solid {color_map.get(status, '#6c757d')};">
            <div class="live-indicator">LIVE</div>
            <h4 style="margin: 0; color: #666;">{label}</h4>
            <h2 style="margin: 0.5rem 0; color: {color_map.get(status, '#333')};">{display_value}</h2>
            <p style="margin: 0; font-size: 0.9rem; color: {delta_color};">
                {delta_sign}{delta:.2f}% vs last period
            </p>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; color: #666;">
                {tooltip}
            </p>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.7rem; color: #999;">
                🕐 Updated: {time_display}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    def render_realtime_alerts(self, data: Optional[Dict[str, Any]]):
        """Render alerts with timestamps"""
        st.markdown("### 🚨 Real-Time Alerts & Notifications")
        
        alerts = data.get('alerts', []) if data else self._get_realtime_alerts()
        
        if not alerts:
            st.success("✅ No critical alerts at this time")
        else:
            for alert in alerts:
                alert_time = alert.get('timestamp', datetime.now())
                time_display = alert_time.strftime('%H:%M:%S')
                
                alert_class = f"alert-{alert['level']}"
                st.markdown(f"""
                <div class="alert-banner {alert_class}">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{alert['title']}</strong><br>
                            {alert['message']}
                        </div>
                        <div style="text-align: right; font-size: 0.8rem; opacity: 0.8;">
                            🕐 {time_display}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
    def render_realtime_charts(self, data: Optional[Dict[str, Any]]):
        """Render charts with real-time data"""
        st.markdown("### 📈 Real-Time Performance Trends")
        
        if PLOTLY_AVAILABLE:
            tab1, tab2, tab3 = st.tabs(["Live Metrics", "Trend Analysis", "Comparison"])
            
            with tab1:
                self._render_live_metrics_chart()
                
            with tab2:
                self._render_realtime_trend_chart()
                
            with tab3:
                self._render_peer_comparison_chart()
        else:
            st.warning("⚠️ Install plotly for real-time charts: pip install plotly")
            self._render_basic_charts()
            
    def render_realtime_risk_dashboard(self, data: Optional[Dict[str, Any]]):
        """Render risk dashboard with real-time updates"""
        st.markdown("### ⚠️ Real-Time Risk Assessment")
        
        risk_data = self._get_realtime_risk_data()
        
        # Overall risk score with live indicator
        risk_score = risk_data['overall_score']
        risk_level = risk_data['risk_level']
        last_update = risk_data['last_update']
        
        color_map = {'LOW': '#28a745', 'MEDIUM': '#ffc107', 'HIGH': '#dc3545'}
        progress_color = color_map.get(risk_level, '#ffc107')
        
        st.markdown(f"""
        <div style="background: #f0f0f0; border-radius: 10px; padding: 1rem; margin-bottom: 1rem; position: relative;">
            <div class="live-indicator">LIVE</div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span><strong>Overall Risk Score</strong></span>
                <span style="font-weight: bold; color: {progress_color};">{risk_score}/100</span>
            </div>
            <div style="background: #ddd; border-radius: 5px; height: 20px; overflow: hidden;">
                <div style="background: {progress_color}; width: {risk_score}%; height: 100%;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 0.5rem;">
                <span style="color: {progress_color}; font-weight: bold;">{risk_level} RISK</span>
                <span style="font-size: 0.8rem; color: #666;">🕐 {last_update.strftime('%H:%M:%S')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Risk categories with real-time updates
        st.markdown("#### Risk Categories")
        for category, score in risk_data['categories'].items():
            color = '#dc3545' if score > 70 else '#ffc107' if score > 40 else '#28a745'
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin: 0.5rem 0;">
                <span>{category}</span>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="width: 100px; background: #ddd; border-radius: 5px; height: 10px;">
                        <div style="background: {color}; width: {score}%; height: 100%; border-radius: 5px;"></div>
                    </div>
                    <span style="color: {color}; font-weight: bold;">{score}</span>
                    <span style="font-size: 0.7rem; color: #999;">🔴</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    def render_live_insights(self, data: Optional[Dict[str, Any]]):
        """Render AI insights with real-time updates"""
        st.markdown("### 💡 Live AI Insights")
        
        insights = self._get_realtime_insights()
        
        for insight in insights:
            timestamp = insight.get('timestamp', datetime.now())
            time_display = timestamp.strftime('%H:%M:%S')
            
            with st.expander(f"{insight['icon']} {insight['title']} • {time_display}", expanded=True):
                st.write(insight['content'])
                if insight.get('recommendation'):
                    st.info(f"💡 **Live Recommendation:** {insight['recommendation']}")
                    
                # Confidence score
                confidence = insight.get('confidence', 85)
                st.progress(confidence / 100)
                st.caption(f"AI Confidence: {confidence}%")
                
    def render_trend_analysis(self, data: Optional[Dict[str, Any]]):
        """Render trend analysis with real-time data"""
        st.markdown("### 📊 Real-Time Trend Analysis")
        
        # Get trend data
        trend_data = self._get_trend_data()
        
        if PLOTLY_AVAILABLE:
            # Create trend chart
            fig = go.Figure()
            
            for metric, values in trend_data.items():
                fig.add_trace(go.Scatter(
                    x=list(range(len(values))),
                    y=values,
                    mode='lines+markers',
                    name=metric,
                    line=dict(width=2)
                ))
            
            fig.update_layout(
                title="Real-Time Trend Analysis (Last 30 minutes)",
                xaxis_title="Time Points",
                yaxis_title="Values",
                hovermode='x unified',
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Fallback table view
            df = pd.DataFrame(trend_data)
            st.dataframe(df.tail(10), use_container_width=True)
            
    def render_realtime_footer(self):
        """Render footer with system status"""
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🔴 System Status", "ONLINE", "Real-Time Active")
            
        with col2:
            data_points = len(st.session_state.get('realtime_data', []))
            st.metric("📊 Data Points", data_points, "Collected")
            
        with col3:
            uptime = "2h 34m"  # Mock uptime
            st.metric("⏱️ Uptime", uptime, "Since Start")
            
        with col4:
            current_time = datetime.now()
            st.metric("🕐 Server Time", current_time.strftime('%H:%M:%S'), current_time.strftime('%Y-%m-%d'))
        
        st.markdown("""
        <div style='text-align: center; color: #666; font-size: 0.9rem; margin-top: 1rem;'>
            <p>© 2024 BPKH - Bank Muamalat Real-Time Monitoring System</p>
            <p>🔴 LIVE MODE | Powered by RAG & Agentic AI | Real-Time Analytics</p>
        </div>
        """, unsafe_allow_html=True)
        
    # Helper methods for real-time functionality
    def _generate_new_data_point(self):
        """Generate new real-time data point"""
        import random
        
        # Initialize session state
        if 'realtime_data' not in st.session_state:
            st.session_state.realtime_data = []
        
        # Generate new data
        new_data = {
            'timestamp': datetime.now(),
            'car': 29.42 + random.uniform(-0.5, 0.5),
            'npf': 3.99 + random.uniform(-0.1, 0.1),
            'roa': 0.03 + random.uniform(-0.01, 0.01),
            'bopo': 98.5 + random.uniform(-1.0, 1.0)
        }
        
        # Add to session state
        st.session_state.realtime_data.append(new_data)
        
        # Keep only last 100 points
        if len(st.session_state.realtime_data) > 100:
            st.session_state.realtime_data = st.session_state.realtime_data[-100:]
    
    def _get_realtime_mock_data(self) -> Dict[str, Any]:
        """Get real-time mock data"""
        return {
            'metrics': {
                'car': 29.42,
                'car_delta': 2.5,
                'npf': 3.99,
                'npf_delta': 0.5,
                'roa': 0.03,
                'roa_delta': -0.02,
                'roe': 0.4,
                'roe_delta': -0.1,
                'bopo': 98.5,
                'bopo_delta': 1.2,
                'fdr': 85.0,
                'fdr_delta': -2.3
            },
            'timestamp': datetime.now()
        }
    
    def _get_realtime_alerts(self) -> list:
        """Get real-time alerts with timestamps"""
        return [
            {
                'level': 'critical',
                'title': 'NPF Threshold Alert',
                'message': 'NPF approaching 4.0% - monitoring closely',
                'timestamp': datetime.now() - timedelta(minutes=2)
            },
            {
                'level': 'warning',
                'title': 'BOPO Efficiency Alert', 
                'message': 'Operational costs trending upward',
                'timestamp': datetime.now() - timedelta(minutes=5)
            }
        ]
    
    def _get_realtime_risk_data(self) -> Dict[str, Any]:
        """Get real-time risk data"""
        return {
            'overall_score': 65,
            'risk_level': 'MEDIUM',
            'last_update': datetime.now(),
            'categories': {
                'Credit Risk': 75,
                'Operational Risk': 70,
                'Market Risk': 45,
                'Liquidity Risk': 30,
                'Compliance Risk': 50
            }
        }
    
    def _get_realtime_insights(self) -> list:
        """Get real-time AI insights"""
        return [
            {
                'icon': '📈',
                'title': 'Capital Position Stable',
                'content': 'CAR maintains strong position above regulatory requirements.',
                'recommendation': 'Monitor for growth opportunities.',
                'confidence': 92,
                'timestamp': datetime.now() - timedelta(minutes=1)
            },
            {
                'icon': '⚠️',
                'title': 'NPF Trend Alert',
                'content': 'Asset quality showing stress signals in corporate segment.',
                'recommendation': 'Implement enhanced monitoring procedures.',
                'confidence': 87,
                'timestamp': datetime.now() - timedelta(minutes=3)
            }
        ]
    
    def _get_trend_data(self) -> Dict[str, list]:
        """Get trend data for analysis"""
        import random
        
        # Generate trend data for last 30 points
        points = 30
        return {
            'CAR': [29.42 + random.uniform(-0.3, 0.3) for _ in range(points)],
            'NPF': [3.99 + random.uniform(-0.1, 0.1) for _ in range(points)],
            'BOPO': [98.5 + random.uniform(-0.5, 0.5) for _ in range(points)]
        }
    
    def _export_realtime_data(self):
        """Export real-time data"""
        if 'realtime_data' in st.session_state:
            import json
            export_data = {
                'export_time': datetime.now().isoformat(),
                'total_points': len(st.session_state.realtime_data),
                'data': st.session_state.realtime_data
            }
            
            st.download_button(
                "💾 Download Real-Time Data",
                json.dumps(export_data, indent=2, default=str),
                f"realtime_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "application/json"
            )
        else:
            st.warning("No real-time data available for export")
    
    def _render_live_metrics_chart(self):
        """Render live metrics chart"""
        if not PLOTLY_AVAILABLE:
            return
        
        # Get real-time data
        data = st.session_state.get('realtime_data', [])
        
        if len(data) < 2:
            st.info("Collecting real-time data... Please wait.")
            return
        
        # Create DataFrame
        df = pd.DataFrame(data[-30:])  # Last 30 points
        
        # Create chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['car'],
            name='CAR (%)',
            line=dict(color='#28a745', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['npf'] * 10,  # Scale for visibility
            name='NPF (x10)',
            line=dict(color='#dc3545', width=2)
        ))
        
        fig.update_layout(
            title="Live Metrics (Last 30 updates)",
            xaxis_title="Time Points",
            yaxis_title="Values",
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_realtime_trend_chart(self):
        """Render real-time trend chart"""
        # Implementation similar to live metrics but with different view
        st.info("📈 Real-time trend analysis coming soon...")
    
    def _render_peer_comparison_chart(self):
        """Render peer comparison chart"""
        # Implementation for peer comparison
        st.info("📊 Peer comparison with real-time benchmarks coming soon...")
    
    def _render_basic_charts(self):
        """Render basic charts when plotly not available"""
        st.info("📊 Basic charts mode - Install plotly for advanced real-time visualizations")

# Standalone render function for direct use
def render_realtime_dashboard(config, data: Optional[Dict[str, Any]] = None):
    """Render real-time dashboard with given configuration and data"""
    dashboard = RealTimeDashboard(config)
    dashboard.render(data)