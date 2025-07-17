"""
Unified Charts Module for Bank Muamalat Health Monitoring
Combines original chart functions with error-safe utilities
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Any, Callable, Optional, List, Dict
import logging

# Setup logger
logger = logging.getLogger(__name__)

# =============================================================================
# ORIGINAL CHART FUNCTIONS (Enhanced with Error Handling)
# =============================================================================

def create_gauge_chart(
    value: float, 
    title: str = "Score", 
    threshold: float = 70.0,
    min_val: float = 0.0,
    max_val: float = 100.0,
    color: str = "darkblue"
) -> Optional[go.Figure]:
    """
    Create a gauge chart (Enhanced version of original)
    
    Args:
        value: Current value to display
        title: Chart title
        threshold: Threshold line value
        min_val: Minimum gauge value
        max_val: Maximum gauge value
        color: Gauge bar color
    
    Returns:
        Plotly figure or None if error
    """
    try:
        # Validate inputs
        if not isinstance(value, (int, float)):
            raise ValueError(f"Value must be numeric, got {type(value)}")
        
        if value < min_val or value > max_val:
            logger.warning(f"Value {value} outside range [{min_val}, {max_val}]")
        
        # Clamp value to range
        clamped_value = max(min_val, min(max_val, value))
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=clamped_value,
            title={'text': title, 'font': {'size': 16}},
            delta={'reference': threshold, 'relative': True},
            gauge={
                'axis': {'range': [min_val, max_val]},
                'bar': {'color': color},
                'steps': [
                    {'range': [min_val, threshold * 0.6], 'color': "lightgray"},
                    {'range': [threshold * 0.6, threshold], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': threshold
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
            font=dict(size=12)
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Gauge chart creation error: {str(e)}")
        return None

def create_trend_chart(
    x: List[Any], 
    y: List[float], 
    title: str = "Trend", 
    y_title: str = "Value",
    x_title: str = "Time",
    color: str = "blue",
    show_markers: bool = True
) -> Optional[go.Figure]:
    """
    Create a trend chart (Enhanced version of original)
    
    Args:
        x: X-axis data (time/categories)
        y: Y-axis data (values)
        title: Chart title
        y_title: Y-axis title
        x_title: X-axis title
        color: Line color
        show_markers: Whether to show markers
    
    Returns:
        Plotly figure or None if error
    """
    try:
        # Validate inputs
        if not x or not y:
            raise ValueError("X and Y data cannot be empty")
        
        if len(x) != len(y):
            raise ValueError(f"X and Y data length mismatch: {len(x)} vs {len(y)}")
        
        # Convert to pandas for easier handling
        df = pd.DataFrame({'x': x, 'y': y})
        
        fig = go.Figure()
        
        mode = "lines+markers" if show_markers else "lines"
        
        fig.add_trace(go.Scatter(
            x=df['x'], 
            y=df['y'], 
            mode=mode,
            name=y_title,
            line=dict(color=color, width=2),
            marker=dict(size=6) if show_markers else None
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title=x_title,
            yaxis_title=y_title,
            height=300,
            hovermode='x unified',
            margin=dict(l=40, r=40, t=40, b=40),
            font=dict(size=12)
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Trend chart creation error: {str(e)}")
        return None

# =============================================================================
# SAFE CHART UTILITIES (From chart_utils.py)
# =============================================================================

def safe_render_chart(
    chart_func: Callable,
    fallback_message: str,
    *args,
    **kwargs
) -> Optional[Any]:
    """
    Safely render chart with error handling and fallback
    
    Args:
        chart_func: Function to render the chart
        fallback_message: Message to show if chart fails
        *args: Arguments for chart function
        **kwargs: Keyword arguments for chart function
    
    Returns:
        Chart figure or None if error
    """
    try:
        return chart_func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Chart rendering error: {str(e)}")
        st.error(f"Chart rendering error: {str(e)}")
        st.info(fallback_message)
        return None

def safe_plotly_chart(
    fig: go.Figure,
    fallback_message: str = "Chart data unavailable",
    **kwargs
) -> None:
    """
    Safely display plotly chart with error handling
    
    Args:
        fig: Plotly figure object
        fallback_message: Message to show if display fails
        **kwargs: Additional arguments for st.plotly_chart
    """
    try:
        if fig is not None:
            # Set default kwargs
            chart_kwargs = {
                'use_container_width': True,
                'config': {'displayModeBar': False}
            }
            chart_kwargs.update(kwargs)
            
            st.plotly_chart(fig, **chart_kwargs)
        else:
            st.info(fallback_message)
    except Exception as e:
        logger.error(f"Plotly chart display error: {str(e)}")
        st.error(f"Chart display error: {str(e)}")
        st.info(fallback_message)

def create_safe_bar_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    color: Optional[str] = None,
    **kwargs
) -> Optional[go.Figure]:
    """
    Create bar chart with error handling
    
    Args:
        data: DataFrame with chart data
        x: Column name for x-axis
        y: Column name for y-axis
        title: Chart title
        color: Column name for color coding
        **kwargs: Additional plotly express arguments
    
    Returns:
        Plotly figure or None if error
    """
    try:
        # Validate data
        if data.empty:
            raise ValueError("Data is empty")
        
        if x not in data.columns or y not in data.columns:
            raise ValueError(f"Columns '{x}' or '{y}' not found in data")
        
        # Create chart
        chart_kwargs = {
            'title': title,
            'color_discrete_sequence': px.colors.qualitative.Set2
        }
        chart_kwargs.update(kwargs)
        
        if color and color in data.columns:
            fig = px.bar(data, x=x, y=y, color=color, **chart_kwargs)
        else:
            fig = px.bar(data, x=x, y=y, **chart_kwargs)
        
        # Update layout for better appearance
        fig.update_layout(
            xaxis_title=x.replace('_', ' ').title(),
            yaxis_title=y.replace('_', ' ').title(),
            font=dict(size=12),
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Bar chart creation error: {str(e)}")
        return None

def create_safe_line_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    **kwargs
) -> Optional[go.Figure]:
    """
    Create line chart with error handling
    
    Args:
        data: DataFrame with chart data
        x: Column name for x-axis
        y: Column name for y-axis
        title: Chart title
        **kwargs: Additional plotly arguments
    
    Returns:
        Plotly figure or None if error
    """
    try:
        # Validate data
        if data.empty:
            raise ValueError("Data is empty")
        
        if x not in data.columns or y not in data.columns:
            raise ValueError(f"Columns '{x}' or '{y}' not found in data")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=data[x],
            y=data[y],
            mode='lines+markers',
            name=y.replace('_', ' ').title(),
            line=dict(width=2),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title=x.replace('_', ' ').title(),
            yaxis_title=y.replace('_', ' ').title(),
            hovermode='x unified',
            font=dict(size=12),
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Line chart creation error: {str(e)}")
        return None

def create_safe_pie_chart(
    data: pd.DataFrame,
    values: str,
    names: str,
    title: str = "",
    **kwargs
) -> Optional[go.Figure]:
    """
    Create pie chart with error handling
    
    Args:
        data: DataFrame with chart data
        values: Column name for values
        names: Column name for labels
        title: Chart title
        **kwargs: Additional plotly express arguments
    
    Returns:
        Plotly figure or None if error
    """
    try:
        # Validate data
        if data.empty:
            raise ValueError("Data is empty")
        
        if values not in data.columns or names not in data.columns:
            raise ValueError(f"Columns '{values}' or '{names}' not found in data")
        
        # Create chart
        chart_kwargs = {
            'title': title,
            'color_discrete_sequence': px.colors.qualitative.Set3
        }
        chart_kwargs.update(kwargs)
        
        fig = px.pie(data, values=values, names=names, **chart_kwargs)
        
        fig.update_layout(
            font=dict(size=12),
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Pie chart creation error: {str(e)}")
        return None

def create_safe_scatter_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    size: Optional[str] = None,
    color: Optional[str] = None,
    **kwargs
) -> Optional[go.Figure]:
    """
    Create scatter plot with error handling
    
    Args:
        data: DataFrame with chart data
        x: Column name for x-axis
        y: Column name for y-axis
        title: Chart title
        size: Column name for point sizes
        color: Column name for color coding
        **kwargs: Additional plotly express arguments
    
    Returns:
        Plotly figure or None if error
    """
    try:
        # Validate data
        if data.empty:
            raise ValueError("Data is empty")
        
        required_cols = [x, y]
        if size:
            required_cols.append(size)
        if color:
            required_cols.append(color)
        
        missing_cols = [col for col in required_cols if col not in data.columns]
        if missing_cols:
            raise ValueError(f"Columns {missing_cols} not found in data")
        
        # Create chart
        chart_kwargs = {
            'title': title,
            'color_discrete_sequence': px.colors.qualitative.Set1
        }
        chart_kwargs.update(kwargs)
        
        fig = px.scatter(data, x=x, y=y, size=size, color=color, **chart_kwargs)
        
        fig.update_layout(
            xaxis_title=x.replace('_', ' ').title(),
            yaxis_title=y.replace('_', ' ').title(),
            font=dict(size=12),
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Scatter chart creation error: {str(e)}")
        return None

# =============================================================================
# ADVANCED CHART FUNCTIONS
# =============================================================================

def create_multi_line_chart(
    data: pd.DataFrame,
    x: str,
    y_columns: List[str],
    title: str = "",
    colors: Optional[List[str]] = None
) -> Optional[go.Figure]:
    """
    Create multi-line chart for trend comparison
    
    Args:
        data: DataFrame with chart data
        x: Column name for x-axis
        y_columns: List of column names for y-axis
        title: Chart title
        colors: List of colors for each line
    
    Returns:
        Plotly figure or None if error
    """
    try:
        if data.empty:
            raise ValueError("Data is empty")
        
        if x not in data.columns:
            raise ValueError(f"X column '{x}' not found in data")
        
        missing_y_cols = [col for col in y_columns if col not in data.columns]
        if missing_y_cols:
            raise ValueError(f"Y columns {missing_y_cols} not found in data")
        
        fig = go.Figure()
        
        # Default colors if not provided
        if not colors:
            colors = px.colors.qualitative.Set1[:len(y_columns)]
        
        for i, y_col in enumerate(y_columns):
            color = colors[i % len(colors)]
            
            fig.add_trace(go.Scatter(
                x=data[x],
                y=data[y_col],
                mode='lines+markers',
                name=y_col.replace('_', ' ').title(),
                line=dict(color=color, width=2),
                marker=dict(size=6)
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title=x.replace('_', ' ').title(),
            yaxis_title="Values",
            hovermode='x unified',
            font=dict(size=12),
            margin=dict(l=40, r=40, t=40, b=40),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Multi-line chart creation error: {str(e)}")
        return None

def create_dual_axis_chart(
    data: pd.DataFrame,
    x: str,
    y1: str,
    y2: str,
    title: str = "",
    y1_title: str = "Y1",
    y2_title: str = "Y2"
) -> Optional[go.Figure]:
    """
    Create chart with dual y-axes
    
    Args:
        data: DataFrame with chart data
        x: Column name for x-axis
        y1: Column name for primary y-axis
        y2: Column name for secondary y-axis
        title: Chart title
        y1_title: Primary y-axis title
        y2_title: Secondary y-axis title
    
    Returns:
        Plotly figure or None if error
    """
    try:
        if data.empty:
            raise ValueError("Data is empty")
        
        required_cols = [x, y1, y2]
        missing_cols = [col for col in required_cols if col not in data.columns]
        if missing_cols:
            raise ValueError(f"Columns {missing_cols} not found in data")
        
        fig = go.Figure()
        
        # Primary y-axis
        fig.add_trace(go.Scatter(
            x=data[x],
            y=data[y1],
            mode='lines+markers',
            name=y1_title,
            line=dict(color='blue', width=2),
            yaxis='y'
        ))
        
        # Secondary y-axis
        fig.add_trace(go.Scatter(
            x=data[x],
            y=data[y2],
            mode='lines+markers',
            name=y2_title,
            line=dict(color='red', width=2),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title=x.replace('_', ' ').title(),
            yaxis=dict(
                title=y1_title,
                side='left',
                color='blue'
            ),
            yaxis2=dict(
                title=y2_title,
                side='right',
                overlaying='y',
                color='red'
            ),
            hovermode='x unified',
            font=dict(size=12),
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Dual axis chart creation error: {str(e)}")
        return None

def display_fallback_metrics(metrics: Dict[str, Any]):
    """
    Display fallback metrics when charts fail
    
    Args:
        metrics: Dictionary of metric names and values
    """
    st.markdown("### 📊 Key Metrics Summary")
    
    if not metrics:
        st.info("No metrics data available")
        return
    
    # Display in columns
    cols = st.columns(min(len(metrics), 4))
    
    for i, (key, value) in enumerate(metrics.items()):
        with cols[i % len(cols)]:
            if isinstance(value, dict):
                st.metric(key, value.get('value', 'N/A'), value.get('delta', ''))
            else:
                st.metric(key, value)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def validate_chart_data(data: pd.DataFrame, required_columns: List[str]) -> bool:
    """
    Validate data before chart creation
    
    Args:
        data: DataFrame to validate
        required_columns: List of required column names
    
    Returns:
        True if valid, raises ValueError if not
    """
    if data.empty:
        raise ValueError("Data is empty")
    
    missing_cols = [col for col in required_columns if col not in data.columns]
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")
    
    return True

def apply_chart_theme(fig: go.Figure, theme: str = "default") -> go.Figure:
    """
    Apply consistent theme to charts
    
    Args:
        fig: Plotly figure to theme
        theme: Theme name ("default", "dark", "minimal")
    
    Returns:
        Themed figure
    """
    try:
        if theme == "dark":
            fig.update_layout(
                plot_bgcolor='#2E2E2E',
                paper_bgcolor='#1E1E1E',
                font_color='white'
            )
        elif theme == "minimal":
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(size=10),
                showlegend=False
            )
        else:  # default
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(size=12)
            )
        
        return fig
        
    except Exception as e:
        logger.error(f"Theme application error: {str(e)}")
        return fig

# =============================================================================
# EXPORTS
# =============================================================================

# Export all functions
__all__ = [
    # Original functions (enhanced)
    'create_gauge_chart',
    'create_trend_chart',
    
    # Safe utilities
    'safe_render_chart',
    'safe_plotly_chart',
    'create_safe_bar_chart',
    'create_safe_line_chart',
    'create_safe_pie_chart',
    'create_safe_scatter_chart',
    
    # Advanced functions
    'create_multi_line_chart',
    'create_dual_axis_chart',
    
    # Helper functions
    'display_fallback_metrics',
    'validate_chart_data',
    'apply_chart_theme'
]