"""
Metric cards component for dashboard
"""

import streamlit as st
from typing import Dict, Any, Optional, List
import plotly.graph_objects as go
import plotly.express as px

# Fallback functions for missing helpers
def format_currency(value: float) -> str:
    """Format currency value"""
    if value >= 1e12:
        return f"Rp {value/1e12:.1f}T"
    elif value >= 1e9:
        return f"Rp {value/1e9:.1f}B"
    elif value >= 1e6:
        return f"Rp {value/1e6:.1f}M"
    else:
        return f"Rp {value:,.0f}"

def format_percentage(value: float) -> str:
    """Format percentage value"""
    return f"{value:.2f}%"

def get_risk_color(risk_level: str) -> str:
    """Get color for risk level"""
    colors = {
        'low': '#28a745',
        'medium': '#ffc107', 
        'high': '#dc3545',
        'critical': '#dc3545'
    }
    return colors.get(risk_level.lower(), '#6c757d')

def display_metric_cards(metrics: Dict[str, Any], layout: str = "horizontal"):
    """
    Display metric cards in specified layout
    
    Args:
        metrics: Dictionary of metrics to display
        layout: Layout type ('horizontal', 'vertical', 'grid')
    """
    if not metrics:
        st.warning("No metrics data available")
        return
        
    try:
        if layout == "horizontal":
            cols = st.columns(len(metrics))
            for i, (key, value) in enumerate(metrics.items()):
                with cols[i]:
                    render_single_metric_card(key, value)
        elif layout == "vertical":
            for key, value in metrics.items():
                render_single_metric_card(key, value)
        elif layout == "grid":
            # 3 columns grid
            cols_per_row = 3
            rows = (len(metrics) + cols_per_row - 1) // cols_per_row
            
            metric_items = list(metrics.items())
            idx = 0
            
            for row in range(rows):
                cols = st.columns(cols_per_row)
                for col in range(cols_per_row):
                    if idx < len(metric_items):
                        with cols[col]:
                            key, value = metric_items[idx]
                            render_single_metric_card(key, value)
                        idx += 1
    except Exception as e:
        st.error(f"Error displaying metrics: {str(e)}")

def render_single_metric_card(
    metric_name: str,
    metric_data: Dict[str, Any],
    show_chart: bool = False
):
    """
    Render a single metric card
    
    Args:
        metric_name: Name of the metric
        metric_data: Dictionary containing value, delta, status, etc.
        show_chart: Whether to show mini chart
    """
    try:
        # Extract data with safe defaults
        value = metric_data.get('value', 0)
        delta = metric_data.get('delta', 0)
        status = metric_data.get('status', 'normal')
        unit = metric_data.get('unit', '')
        description = metric_data.get('description', '')
        target = metric_data.get('target')
        trend_data = metric_data.get('trend', [])
        
        # Determine color based on status
        status_colors = {
            'good': '#28a745',
            'warning': '#ffc107',
            'critical': '#dc3545',
            'normal': '#6c757d'
        }
        color = status_colors.get(status, '#6c757d')
        
        # Create card container
        with st.container():
            st.markdown(f"""
            <div style='
                background: white;
                padding: 1.5rem;
                border-radius: 10px;
                border-left: 4px solid {color};
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                margin-bottom: 1rem;
            '>
                <h4 style='margin: 0; color: #666; font-size: 0.9rem;'>{metric_name}</h4>
                <h2 style='margin: 0.5rem 0; color: {color};'>
                    {format_value(value, unit)}
                </h2>
                {format_delta_html(delta, unit)}
                {f'<p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; color: #999;">{description}</p>' if description else ''}
                {format_target_html(value, target, unit) if target else ''}
            </div>
            """, unsafe_allow_html=True)
            
            # Show mini chart if requested and trend data available
            if show_chart and trend_data:
                render_mini_chart(trend_data, metric_name, color)
    except Exception as e:
        st.error(f"Error rendering metric card '{metric_name}': {str(e)}")

def render_metric_group(
    group_title: str,
    metrics: Dict[str, Any],
    columns: int = 4
):
    """
    Render a group of related metrics
    
    Args:
        group_title: Title for the metric group
        metrics: Dictionary of metrics
        columns: Number of columns for layout
    """
    if not metrics:
        st.warning(f"No data available for {group_title}")
        return
        
    try:
        st.markdown(f"### {group_title}")
        
        cols = st.columns(columns)
        for i, (key, value) in enumerate(metrics.items()):
            with cols[i % columns]:
                render_single_metric_card(key, value)
    except Exception as e:
        st.error(f"Error rendering metric group '{group_title}': {str(e)}")

def render_enhanced_metric_card(
    title: str,
    value: float,
    subtitle: str = "",
    delta: Optional[float] = None,
    delta_color: str = "normal",
    progress: Optional[float] = None,
    target: Optional[float] = None,
    icon: str = "📊",
    color_scheme: str = "blue"
):
    """
    Render enhanced metric card with additional features
    """
    try:
        # Color schemes
        color_schemes = {
            'blue': {'primary': '#1f77b4', 'light': '#e3f2fd', 'dark': '#0d47a1'},
            'green': {'primary': '#28a745', 'light': '#d4edda', 'dark': '#155724'},
            'red': {'primary': '#dc3545', 'light': '#f8d7da', 'dark': '#721c24'},
            'yellow': {'primary': '#ffc107', 'light': '#fff3cd', 'dark': '#856404'},
            'purple': {'primary': '#6f42c1', 'light': '#e7e2f3', 'dark': '#4e2a84'}
        }
        
        colors = color_schemes.get(color_scheme, color_schemes['blue'])
        
        # Calculate progress if target provided
        if target and target != 0 and not progress:
            progress = min(100, (value / target) * 100)
        
        # Create card
        card_html = f"""
        <div style='
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-top: 3px solid {colors['primary']};
            position: relative;
            overflow: hidden;
        '>
            <div style='display: flex; align-items: center; margin-bottom: 0.5rem;'>
                <span style='font-size: 2rem; margin-right: 0.5rem;'>{icon}</span>
                <div>
                    <h4 style='margin: 0; color: #333; font-weight: 600;'>{title}</h4>
                    {f'<p style="margin: 0; color: #666; font-size: 0.8rem;">{subtitle}</p>' if subtitle else ''}
                </div>
            </div>
            
            <div style='margin: 1rem 0;'>
                <h2 style='margin: 0; color: {colors["primary"]}; font-size: 2.5rem;'>
                    {format_value(value)}
                </h2>
            </div>
        """
        
        # Add delta if provided
        if delta is not None:
            delta_icon = "↑" if delta > 0 else "↓" if delta < 0 else "→"
            delta_color_map = {
                'normal': colors['primary'],
                'inverse': colors['primary'] if delta < 0 else colors['dark'],
                'positive': '#28a745' if delta > 0 else '#dc3545',
                'negative': '#dc3545' if delta > 0 else '#28a745'
            }
            delta_color_value = delta_color_map.get(delta_color, colors['primary'])
            
            card_html += f"""
            <div style='display: flex; align-items: center; margin: 0.5rem 0;'>
                <span style='color: {delta_color_value}; font-weight: 600;'>
                    {delta_icon} {abs(delta):.1f}%
                </span>
                <span style='color: #999; margin-left: 0.5rem; font-size: 0.8rem;'>
                    vs previous period
                </span>
            </div>
            """
        
        # Add progress bar if provided
        if progress is not None:
            card_html += f"""
            <div style='margin-top: 1rem;'>
                <div style='
                    background: {colors['light']};
                    height: 8px;
                    border-radius: 4px;
                    overflow: hidden;
                '>
                    <div style='
                        background: {colors['primary']};
                        width: {progress}%;
                        height: 100%;
                        transition: width 0.3s ease;
                    '></div>
                </div>
                {f'<p style="margin: 0.25rem 0 0 0; color: #666; font-size: 0.75rem; text-align: right;">{progress:.0f}% of target</p>' if target else ''}
            </div>
            """
        
        # Add decorative background element
        card_html += f"""
            <div style='
                position: absolute;
                right: -20px;
                bottom: -20px;
                width: 100px;
                height: 100px;
                background: {colors['light']};
                border-radius: 50%;
                opacity: 0.3;
            '></div>
        </div>
        """
        
        st.markdown(card_html, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error rendering enhanced metric card '{title}': {str(e)}")

def render_comparison_metrics(
    metrics: List[Dict[str, Any]],
    highlight_best: bool = True
):
    """
    Render metrics with comparison highlighting
    
    Args:
        metrics: List of metric dictionaries with 'name', 'value', 'unit'
        highlight_best: Whether to highlight best performing metric
    """
    if not metrics:
        st.warning("No comparison metrics available")
        return
        
    try:
        # Find best value if highlighting
        best_idx = 0
        if highlight_best and len(metrics) > 1:
            values = [m.get('value', 0) for m in metrics]
            # Determine if higher or lower is better based on metric type
            lower_is_better = ['NPF', 'BOPO', 'Cost', 'Risk']
            metric_name = metrics[0].get('name', '')
            
            if any(lib in metric_name for lib in lower_is_better):
                best_idx = values.index(min(values))
            else:
                best_idx = values.index(max(values))
        
        # Render metrics
        cols = st.columns(len(metrics))
        for i, metric in enumerate(metrics):
            with cols[i]:
                is_best = i == best_idx and highlight_best
                render_comparison_metric_card(metric, is_best)
    except Exception as e:
        st.error(f"Error rendering comparison metrics: {str(e)}")

def render_comparison_metric_card(metric: Dict[str, Any], is_best: bool = False):
    """Render a single comparison metric card"""
    try:
        value = metric.get('value', 0)
        name = metric.get('name', '')
        unit = metric.get('unit', '')
        entity = metric.get('entity', '')
        
        # Styling for best performer
        border_color = '#ffc107' if is_best else '#e0e0e0'
        background = '#fffbf0' if is_best else 'white'
        
        st.markdown(f"""
        <div style='
            background: {background};
            padding: 1rem;
            border-radius: 8px;
            border: 2px solid {border_color};
            text-align: center;
            position: relative;
        '>
            {f'<div style="position: absolute; top: -10px; left: 50%; transform: translateX(-50%); background: #ffc107; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem;">BEST</div>' if is_best else ''}
            <h5 style='margin: 0; color: #666;'>{entity}</h5>
            <h3 style='margin: 0.5rem 0; color: #333;'>{format_value(value, unit)}</h3>
            <p style='margin: 0; color: #999; font-size: 0.8rem;'>{name}</p>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error rendering comparison metric card: {str(e)}")

def render_mini_chart(data: List[float], title: str, color: str):
    """Render a mini sparkline chart"""
    try:
        if not data:
            return
            
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            y=data,
            mode='lines',
            line=dict(color=color, width=2),
            fill='tozeroy',
            fillcolor=f'rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.1)'
        ))
        
        fig.update_layout(
            height=60,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    except Exception as e:
        st.error(f"Error rendering mini chart for '{title}': {str(e)}")

def render_kpi_summary(metrics: Dict[str, Any]):
    """Render KPI summary with status indicators"""
    try:
        st.markdown("### 📊 KPI Summary")
        
        # Calculate overall health score
        total_score = 0
        metric_count = 0
        
        for metric_name, metric_data in metrics.items():
            if isinstance(metric_data, dict):
                status = metric_data.get('status', 'normal')
                if status == 'good':
                    total_score += 100
                elif status == 'warning':
                    total_score += 60
                elif status == 'critical':
                    total_score += 20
                else:
                    total_score += 50
                metric_count += 1
        
        overall_score = total_score / metric_count if metric_count > 0 else 0
        
        # Display overall health
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if overall_score >= 80:
                st.success(f"🟢 Overall Health: {overall_score:.0f}%")
            elif overall_score >= 60:
                st.warning(f"🟡 Overall Health: {overall_score:.0f}%")
            else:
                st.error(f"🔴 Overall Health: {overall_score:.0f}%")
        
        with col2:
            good_count = sum(1 for m in metrics.values() if isinstance(m, dict) and m.get('status') == 'good')
            st.metric("Good Metrics", good_count)
        
        with col3:
            critical_count = sum(1 for m in metrics.values() if isinstance(m, dict) and m.get('status') == 'critical')
            st.metric("Critical Metrics", critical_count)
            
    except Exception as e:
        st.error(f"Error rendering KPI summary: {str(e)}")

# Helper functions
def format_value(value: float, unit: str = '') -> str:
    """Format value with appropriate unit"""
    try:
        if unit == '%':
            return f"{value:.2f}%"
        elif unit == 'IDR':
            return format_currency(value)
        elif unit == 'T' or unit == 'trillion':
            return f"{value:.1f}T"
        elif unit == 'B' or unit == 'billion':
            return f"{value:.1f}B"
        elif unit == 'M' or unit == 'million':
            return f"{value:.1f}M"
        elif unit == 'K' or unit == 'thousand':
            return f"{value:.1f}K"
        else:
            return f"{value:,.2f}{' ' + unit if unit else ''}"
    except:
        return str(value)

def format_delta_html(delta: float, unit: str = '') -> str:
    """Format delta value as HTML"""
    try:
        if delta == 0:
            return ""
            
        arrow = "↑" if delta > 0 else "↓"
        color = "#28a745" if delta > 0 else "#dc3545"
        
        return f"""
        <p style='margin: 0; color: {color}; font-size: 0.9rem;'>
            {arrow} {abs(delta):.1f}{unit} from previous
        </p>
        """
    except:
        return ""

def format_target_html(value: float, target: float, unit: str = '') -> str:
    """Format target comparison as HTML"""
    try:
        if target == 0:
            return ""
            
        percentage = (value / target) * 100
        
        return f"""
        <div style='margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px solid #eee;'>
            <small style='color: #666;'>
                Target: {format_value(target, unit)} ({percentage:.0f}% achieved)
            </small>
        </div>
        """
    except:
        return ""

def create_metric_data(
    value: float,
    unit: str = '',
    delta: float = 0,
    status: str = 'normal',
    description: str = '',
    target: Optional[float] = None,
    trend: Optional[List[float]] = None
) -> Dict[str, Any]:
    """Helper function to create metric data dictionary"""
    return {
        'value': value,
        'unit': unit,
        'delta': delta,
        'status': status,
        'description': description,
        'target': target,
        'trend': trend or []
    }

# Alias for backward compatibility
render_metric_card = render_single_metric_card

# Export main functions
__all__ = [
    'display_metric_cards',
    'render_single_metric_card',
    'render_metric_group',
    'render_enhanced_metric_card',
    'render_comparison_metrics',
    'render_comparison_metric_card',
    'render_mini_chart',
    'render_kpi_summary',
    'render_metric_card',  # Alias
    'create_metric_data',
    'format_value',
    'format_delta_html',
    'format_target_html',
    'format_currency',
    'format_percentage',
    'get_risk_color'
]