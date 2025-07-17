# ui/components/risk_matrix.py

import streamlit as st
import pandas as pd
import plotly.express as px

def render_risk_matrix(risks: dict):
    """Render a colored risk matrix based on level"""
    df = pd.DataFrame([
        {"Risk": k, "Level": v} for k, v in risks.items()
    ])
    color_map = {"LOW": "#28a745", "MEDIUM": "#ffc107", "HIGH": "#dc3545"}

    fig = px.bar(
        df, x="Risk", y=[1]*len(df), color="Level",
        color_discrete_map=color_map, height=300
    )
    fig.update_layout(yaxis_visible=False, yaxis_showticklabels=False)
    st.plotly_chart(fig, use_container_width=True)
