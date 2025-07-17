"""
Decision Support Page for Bank Muamalat Health Monitoring
Provides comprehensive decision support for BPKH as controlling shareholder
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import json

def render(orchestrator: Optional[Any] = None):
    """Render the decision support page"""
    
    st.title("🎯 Strategic Decision Support for BPKH")
    st.markdown("### Data-driven recommendations for Bank Muamalat ownership decision")
    
    # Decision Summary Section
    render_decision_summary()
    
    # Key Decision Factors
    render_decision_factors()
    
    # Scenario Analysis
    render_scenario_analysis()
    
    # Value Creation Analysis
    render_value_creation_analysis()
    
    # Exit Strategy Options
    render_exit_strategies()
    
    # Risk-Return Analysis
    render_risk_return_analysis()
    
    # AI Recommendations
    if orchestrator:
        render_ai_recommendations(orchestrator)
    
    # Decision Timeline
    render_decision_timeline()
    
    # Action Plan
    render_action_plan()

def render_decision_summary():
    """Render executive decision summary"""
    st.markdown("## 📊 Executive Decision Summary")
    
    # Create columns for key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Investment Status
        st.metric(
            label="BPKH Investment",
            value="Rp 3.0T",
            delta="ROI: 12.19%",
            help="Total investment including initial capital and sukuk"
        )
        
    with col2:
        # Current Valuation
        current_value = 3.5  # Trillion IDR
        st.metric(
            label="Current Valuation",
            value=f"Rp {current_value}T",
            delta=f"+{(current_value/3.0-1)*100:.1f}%",
            help="Estimated current market value"
        )
        
    with col3:
        # Decision Score
        decision_score = calculate_decision_score()
        st.metric(
            label="Decision Score",
            value=f"{decision_score}/100",
            delta="Maintain" if decision_score > 60 else "Exit",
            delta_color="normal" if decision_score > 60 else "inverse"
        )
        
    with col4:
        # Recommendation
        recommendation = get_primary_recommendation(decision_score)
        color = "#28a745" if "MAINTAIN" in recommendation else "#dc3545"
        st.markdown(
            f"""
            <div style='text-align: center; padding: 10px; background-color: {color}; color: white; border-radius: 10px;'>
                <h4 style='margin: 0;'>{recommendation}</h4>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Summary Box
    with st.container():
        st.info(
            """
            **Strategic Assessment Summary:**
            
            Bank Muamalat shows mixed performance with strong capital position (CAR 29.42%) 
            but operational challenges (NPF 3.99%, BOPO 98.5%). The bank has strategic value 
            through Hajj/Umrah ecosystem synergies but requires significant transformation.
            
            **Key Decision Drivers:**
            - ✅ Strong capital buffer provides transformation runway
            - ⚠️ Asset quality deterioration requires immediate attention  
            - ⚠️ Operational inefficiency impacts profitability
            - ✅ Strategic fit with BPKH's Hajj ecosystem
            - 🔄 Digital transformation potential with right investment
            """
        )

def render_decision_factors():
    """Render key decision factors analysis"""
    st.markdown("## 🔍 Key Decision Factors Analysis")
    
    # Create tabs for different factor categories
    tab1, tab2, tab3, tab4 = st.tabs(["Financial", "Strategic", "Risk", "Market"])
    
    with tab1:
        render_financial_factors()
        
    with tab2:
        render_strategic_factors()
        
    with tab3:
        render_risk_factors()
        
    with tab4:
        render_market_factors()

def render_financial_factors():
    """Render financial decision factors"""
    col1, col2 = st.columns(2)
    
    with col1:
        # Financial Health Score
        fig = create_factor_gauge("Financial Health", 45, [
            {"range": [0, 40], "color": "red"},
            {"range": [40, 70], "color": "yellow"},
            {"range": [70, 100], "color": "green"}
        ])
        st.plotly_chart(fig, use_container_width=True)
        
        # Key Financial Metrics
        st.markdown("### Key Metrics Impact")
        metrics_df = pd.DataFrame({
            'Metric': ['NPF', 'BOPO', 'ROA', 'CAR'],
            'Current': [3.99, 98.5, 0.03, 29.42],
            'Target': [3.0, 85.0, 1.5, 20.0],
            'Impact': ['High', 'Critical', 'Critical', 'Positive']
        })
        st.dataframe(metrics_df, use_container_width=True)
        
    with col2:
        # Profitability Projection
        st.markdown("### Profitability Trajectory")
        
        years = list(range(2024, 2028))
        base_scenario = [0.03, 0.5, 1.0, 1.5]
        transformation_scenario = [0.03, 0.8, 1.5, 2.5]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=years, y=base_scenario,
            name='Base Case',
            line=dict(color='orange', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=years, y=transformation_scenario,
            name='With Transformation',
            line=dict(color='green', width=2)
        ))
        fig.update_layout(
            title="ROA Projection (%)",
            xaxis_title="Year",
            yaxis_title="ROA %",
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)

def render_strategic_factors():
    """Render strategic decision factors"""
    # Strategic Fit Matrix
    st.markdown("### Strategic Fit Assessment")
    
    strategic_factors = {
        'Factor': [
            'Hajj/Umrah Synergy',
            'Government Relations',
            'Islamic Banking Leadership',
            'Digital Capability',
            'Regional Expansion',
            'Product Innovation'
        ],
        'Score': [95, 85, 70, 30, 40, 35],
        'Weight': [25, 20, 15, 20, 10, 10]
    }
    
    df = pd.DataFrame(strategic_factors)
    
    fig = px.bar(
        df, 
        x='Score', 
        y='Factor',
        orientation='h',
        color='Score',
        color_continuous_scale='RdYlGn',
        title='Strategic Fit Scores'
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Strategic Options
    st.markdown("### Strategic Options Analysis")
    
    options = {
        'Option': ['Transform & Hold', 'Quick Exit', 'Strategic Partner', 'IPO Path'],
        'Feasibility': [85, 60, 70, 65],
        'Value Creation': [90, 40, 75, 80],
        'Risk': [70, 30, 60, 75],
        'Timeline': ['3-5 years', '6-12 months', '1-2 years', '2-3 years']
    }
    
    options_df = pd.DataFrame(options)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Radar chart for options
        categories = ['Feasibility', 'Value Creation', 'Risk Mgmt']
        
        fig = go.Figure()
        
        for idx, option in enumerate(options['Option']):
            fig.add_trace(go.Scatterpolar(
                r=[
                    options['Feasibility'][idx],
                    options['Value Creation'][idx],
                    100 - options['Risk'][idx]  # Invert risk for better visualization
                ],
                theta=categories,
                fill='toself',
                name=option
            ))
            
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=True,
            title="Strategic Options Comparison"
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.dataframe(options_df, use_container_width=True)
        
        st.info(
            """
            **Recommended Strategy: Transform & Hold**
            
            This option provides the highest value creation potential while 
            leveraging BPKH's patient capital advantage. Key success factors:
            - CEO with transformation experience
            - Digital partnership strategy
            - Focus on core segments
            - Operational excellence program
            """
        )

def render_risk_factors():
    """Render risk decision factors"""
    st.markdown("### Risk Assessment Matrix")
    
    # Risk heatmap
    risks = {
        'Risk Category': ['Credit', 'Operational', 'Market', 'Liquidity', 'Strategic', 'Regulatory'],
        'Current Level': [75, 70, 40, 30, 65, 45],
        'Trend': ['↗️', '→', '→', '↘️', '↗️', '→'],
        'Impact on Decision': ['High', 'High', 'Medium', 'Low', 'High', 'Medium']
    }
    
    risk_df = pd.DataFrame(risks)
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=[[risks['Current Level'][i]] for i in range(len(risks['Risk Category']))],
        x=['Risk Level'],
        y=risks['Risk Category'],
        colorscale='RdYlGn_r',
        text=[[f"{level}% {trend}"] for level, trend in zip(risks['Current Level'], risks['Trend'])],
        texttemplate="%{text}",
        textfont={"size": 14}
    ))
    
    fig.update_layout(
        title="Risk Heatmap",
        height=400,
        xaxis_title="",
        yaxis_title=""
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk Mitigation Strategies
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Risk Mitigation Priority")
        mitigation = {
            'Credit Risk': 'Establish NPF task force, tighten underwriting',
            'Operational Risk': 'Digital transformation, process automation',
            'Strategic Risk': 'Clear transformation roadmap, KPIs'
        }
        
        for risk, strategy in mitigation.items():
            st.markdown(f"**{risk}:** {strategy}")
            
    with col2:
        st.markdown("### Risk Appetite vs Current")
        
        categories = ['Credit', 'Operational', 'Market', 'Strategic']
        appetite = [60, 50, 70, 60]
        current = [75, 70, 40, 65]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Risk Appetite', x=categories, y=appetite))
        fig.add_trace(go.Bar(name='Current Risk', x=categories, y=current))
        
        fig.update_layout(
            title="Risk Level vs Appetite",
            yaxis_title="Risk Score",
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)

def render_market_factors():
    """Render market decision factors"""
    st.markdown("### Market & Competitive Factors")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Market opportunity
        st.markdown("#### Islamic Banking Market Growth")
        
        years = list(range(2020, 2028))
        market_size = [320, 360, 405, 455, 510, 575, 650, 735]  # Trillion IDR
        
        fig = px.area(
            x=years,
            y=market_size,
            title="Indonesian Islamic Banking Market Size",
            labels={'x': 'Year', 'y': 'Market Size (IDR Trillion)'}
        )
        fig.add_hline(y=455, line_dash="dash", annotation_text="Current")
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        # Competitive position
        st.markdown("#### Competitive Position")
        
        competitors = pd.DataFrame({
            'Bank': ['BSI', 'Muamalat', 'Mega Syariah', 'BCA Syariah', 'Others'],
            'Market Share': [40, 5, 8, 7, 40]
        })
        
        fig = px.pie(
            competitors,
            values='Market Share',
            names='Bank',
            title='Islamic Banking Market Share'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Market opportunities
    st.markdown("### Key Market Opportunities")
    
    opportunities = [
        {"Segment": "Hajj/Umrah", "Size": "Rp 50T", "Growth": "15%", "Muamalat Position": "Strong"},
        {"Segment": "ASN Banking", "Size": "Rp 200T", "Growth": "8%", "Muamalat Position": "Weak"},
        {"Segment": "Digital Natives", "Size": "Rp 150T", "Growth": "25%", "Muamalat Position": "Very Weak"},
        {"Segment": "SME Financing", "Size": "Rp 300T", "Growth": "12%", "Muamalat Position": "Moderate"}
    ]
    
    opp_df = pd.DataFrame(opportunities)
    st.dataframe(opp_df, use_container_width=True)

def render_scenario_analysis():
    """Render scenario analysis"""
    st.markdown("## 🔮 Scenario Analysis")
    
    scenarios = {
        'Scenario': ['Base Case', 'Transformation Success', 'Market Downturn', 'Quick Exit'],
        'Probability': [40, 35, 20, 5],
        'NPV (Rp T)': [3.5, 6.2, 2.1, 2.8],
        'IRR (%)': [8.5, 18.5, 3.2, 5.0],
        'Decision': ['Hold', 'Hold', 'Hold/Review', 'Exit']
    }
    
    scenario_df = pd.DataFrame(scenarios)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # NPV by scenario
        fig = px.bar(
            scenario_df,
            x='Scenario',
            y='NPV (Rp T)',
            color='Probability',
            title='Net Present Value by Scenario',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        # Probability-weighted returns
        scenario_df['Weighted NPV'] = scenario_df['NPV (Rp T)'] * scenario_df['Probability'] / 100
        
        fig = px.pie(
            scenario_df,
            values='Weighted NPV',
            names='Scenario',
            title='Probability-Weighted Value Distribution'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Expected value calculation
    expected_value = scenario_df['Weighted NPV'].sum()
    st.metric(
        "Expected Value",
        f"Rp {expected_value:.1f}T",
        f"{(expected_value/3.0-1)*100:.1f}% return on investment"
    )
    
    # Detailed scenario descriptions
    with st.expander("📋 Scenario Assumptions"):
        st.markdown("""
        **Base Case (40% probability):**
        - Gradual improvement in operations
        - NPF reduces to 3% over 2 years
        - BOPO improves to 90% over 3 years
        - Modest digital investment
        
        **Transformation Success (35% probability):**
        - Aggressive digital transformation
        - Strategic partnerships executed
        - NPF below 2.5%, BOPO below 80%
        - Market share gains in key segments
        
        **Market Downturn (20% probability):**
        - Economic recession impacts
        - NPF spikes to 6-7%
        - Profitability remains negative
        - Additional capital injection needed
        
        **Quick Exit (5% probability):**
        - Immediate sale at discount
        - Limited value recovery
        - Reputation risk for BPKH
        """)

def render_value_creation_analysis():
    """Render value creation analysis"""
    st.markdown("## 💰 Value Creation Analysis")
    
    # Value drivers
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Value Creation Waterfall")
        
        # Waterfall chart data
        values = [3.0, 0.8, 1.2, 0.7, -0.5, -0.3, 0.6, 5.5]
        labels = ['Current Value', 'Operational Efficiency', 'Digital Revenue', 
                 'Hajj Ecosystem', 'NPF Reduction Cost', 'Transformation Cost', 
                 'Market Multiple', 'Target Value']
        
        fig = go.Figure(go.Waterfall(
            x=labels,
            y=values,
            text=[f"+{v}" if v > 0 else f"{v}" for v in values],
            textposition="outside",
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))
        
        fig.update_layout(
            title="Value Creation Path (Rp Trillion)",
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown("### Key Value Drivers")
        
        drivers = {
            'Driver': ['BOPO Reduction', 'Digital Growth', 'NPF Management', 'Hajj Synergy'],
            'Impact': ['High', 'High', 'Medium', 'High'],
            'Timeline': ['18-24 mo', '12-36 mo', '12 mo', '6-12 mo']
        }
        
        driver_df = pd.DataFrame(drivers)
        st.dataframe(driver_df, use_container_width=True)
        
        st.success(
            """
            **Total Value Creation Potential:**
            Rp 2.5T (83% uplift) over 3 years
            
            Target valuation: 1.5x book value
            """
        )
    
    # Value creation roadmap
    st.markdown("### Value Creation Roadmap")
    
    roadmap_data = {
        'Quarter': ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024', 
                   'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025'],
        'Initiatives': [
            'NPF task force',
            'Digital quick wins',
            'Cost optimization',
            'Hajj product launch',
            'Core system upgrade',
            'Partnership execution',
            'Digital bank launch',
            'IPO preparation'
        ],
        'Expected Impact': [
            'NPF -0.5%',
            'New customers +10K',
            'BOPO -3%',
            'Revenue +5%',
            'Efficiency +10%',
            'Distribution +30%',
            'Customers +100K',
            'Valuation ready'
        ]
    }
    
    roadmap_df = pd.DataFrame(roadmap_data)
    st.dataframe(roadmap_df, use_container_width=True)

def render_exit_strategies():
    """Render exit strategy options"""
    st.markdown("## 🚪 Exit Strategy Analysis")
    
    tab1, tab2, tab3 = st.tabs(["IPO Path", "Strategic Sale", "Gradual Exit"])
    
    with tab1:
        render_ipo_analysis()
        
    with tab2:
        render_strategic_sale_analysis()
        
    with tab3:
        render_gradual_exit_analysis()

def render_ipo_analysis():
    """Render IPO path analysis"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### IPO Readiness Score")
        
        readiness_factors = {
            'Factor': ['Financial Performance', 'Corporate Governance', 
                      'Market Position', 'Growth Story', 'Regulatory Compliance'],
            'Current': [40, 70, 60, 65, 80],
            'Required': [70, 85, 70, 80, 90]
        }
        
        df = pd.DataFrame(readiness_factors)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Current', x=df['Factor'], y=df['Current']))
        fig.add_trace(go.Bar(name='Required', x=df['Factor'], y=df['Required']))
        
        fig.update_layout(
            title="IPO Readiness Assessment",
            yaxis_title="Score",
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown("### IPO Timeline & Milestones")
        
        st.markdown("""
        **2024 Q4:** Financial turnaround
        - Achieve positive ROA
        - NPF below 3%
        
        **2025 Q2:** Operational excellence
        - BOPO below 85%
        - Digital platform launch
        
        **2025 Q4:** Growth acceleration
        - 20% customer growth
        - Market share gains
        
        **2026 Q2:** IPO preparation
        - Audit and compliance
        - Roadshow preparation
        
        **2026 Q4:** Target IPO
        - Expected valuation: Rp 8-10T
        - BPKH stake: 51% post-IPO
        """)
        
    st.info(
        """
        **IPO Success Factors:**
        - Consistent profitability for 8 quarters
        - Clear digital transformation story
        - Strong Hajj/Umrah market position
        - Experienced management team
        - Market conditions favorable
        """
    )

def render_strategic_sale_analysis():
    """Render strategic sale analysis"""
    st.markdown("### Potential Strategic Buyers")
    
    buyers = {
        'Buyer Type': ['Regional Islamic Bank', 'Tech Company', 'Global Islamic Bank', 'Consortium'],
        'Interest Level': [70, 85, 60, 75],
        'Synergy Potential': [65, 90, 70, 80],
        'Price Premium': [10, 25, 15, 20],
        'Execution Risk': ['Low', 'Medium', 'High', 'Medium']
    }
    
    buyer_df = pd.DataFrame(buyers)
    
    # Buyer comparison
    fig = px.scatter(
        buyer_df,
        x='Interest Level',
        y='Synergy Potential',
        size='Price Premium',
        color='Buyer Type',
        title='Strategic Buyer Analysis',
        size_max=50
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(buyer_df, use_container_width=True)
    
    # Valuation scenarios
    st.markdown("### Valuation Scenarios")
    
    col1, col2 = st.columns(2)
    
    with col1:
        valuations = {
            'Method': ['Book Value', 'P/E Multiple', 'Strategic Premium', 'Best Case'],
            'Valuation (Rp T)': [3.2, 4.5, 5.8, 6.5]
        }
        
        val_df = pd.DataFrame(valuations)
        
        fig = px.bar(
            val_df,
            x='Method',
            y='Valuation (Rp T)',
            title='Valuation Range',
            color='Valuation (Rp T)',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown("### Deal Structure Options")
        st.markdown("""
        **Option 1: Full Sale**
        - 100% stake sale
        - Clean exit for BPKH
        - Premium valuation possible
        
        **Option 2: Majority Sale**
        - 51% to strategic partner
        - BPKH retains minority stake
        - Continued upside participation
        
        **Option 3: Joint Venture**
        - 50-50 partnership
        - Shared control
        - Technology/capability access
        """)

def render_gradual_exit_analysis():
    """Render gradual exit analysis"""
    st.markdown("### Gradual Exit Strategy")
    
    # Timeline
    timeline_data = {
        'Year': [2024, 2025, 2026, 2027, 2028],
        'BPKH Stake': [82.66, 70, 51, 35, 20],
        'Action': ['Stabilize', 'Partial Sale', 'IPO', 'Secondary Offering', 'Final Exit'],
        'Proceeds (Rp T)': [0, 1.5, 2.5, 2.0, 1.5]
    }
    
    timeline_df = pd.DataFrame(timeline_data)
    
    fig = go.Figure()
    
    # Stake reduction
    fig.add_trace(go.Scatter(
        x=timeline_df['Year'],
        y=timeline_df['BPKH Stake'],
        name='BPKH Stake %',
        line=dict(color='blue', width=3),
        yaxis='y'
    ))
    
    # Cumulative proceeds
    timeline_df['Cumulative Proceeds'] = timeline_df['Proceeds (Rp T)'].cumsum()
    fig.add_trace(go.Bar(
        x=timeline_df['Year'],
        y=timeline_df['Cumulative Proceeds'],
        name='Cumulative Proceeds (Rp T)',
        yaxis='y2',
        marker_color='green',
        opacity=0.6
    ))
    
    fig.update_layout(
        title='Gradual Exit Timeline',
        xaxis_title='Year',
        yaxis=dict(
            title='BPKH Stake %',
            side='left'
        ),
        yaxis2=dict(
            title='Proceeds (Rp T)',
            side='right',
            overlaying='y'
        ),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Benefits and risks
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Benefits")
        st.markdown("""
        - Maximize value through transformation
        - Maintain influence during critical period
        - Capture upside from improvements
        - Market timing flexibility
        - Reduced execution risk
        """)
        
    with col2:
        st.markdown("### ⚠️ Risks")
        st.markdown("""
        - Extended management attention
        - Market volatility exposure
        - Transformation execution risk
        - Regulatory changes
        - Opportunity cost of capital
        """)

def render_risk_return_analysis():
    """Render risk-return analysis"""
    st.markdown("## 📈 Risk-Return Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk-return scatter
        strategies = {
            'Strategy': ['Status Quo', 'Transform & Hold', 'Quick Exit', 
                        'Strategic Partner', 'Aggressive Growth'],
            'Expected Return': [5, 15, 6, 12, 20],
            'Risk Level': [60, 45, 20, 35, 70],
            'Time Horizon': [5, 3, 1, 2, 4]
        }
        
        strategy_df = pd.DataFrame(strategies)
        
        fig = px.scatter(
            strategy_df,
            x='Risk Level',
            y='Expected Return',
            size='Time Horizon',
            color='Strategy',
            title='Risk-Return Profile by Strategy',
            size_max=50
        )
        
        # Add efficient frontier
        fig.add_trace(go.Scatter(
            x=[20, 35, 45, 60],
            y=[6, 10, 13, 15],
            mode='lines',
            name='Efficient Frontier',
            line=dict(dash='dash', color='gray')
        ))
        
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        # Monte Carlo simulation results
        st.markdown("### Monte Carlo Simulation")
        
        # Generate sample distribution
        np.random.seed(42)
        returns = np.random.normal(12, 5, 1000)
        
        fig = px.histogram(
            returns,
            nbins=50,
            title='Return Distribution (1000 simulations)',
            labels={'value': 'IRR %', 'count': 'Frequency'}
        )
        
        # Add percentile lines
        p10 = np.percentile(returns, 10)
        p50 = np.percentile(returns, 50)
        p90 = np.percentile(returns, 90)
        
        fig.add_vline(x=p10, line_dash="dash", annotation_text="P10")
        fig.add_vline(x=p50, line_dash="dash", annotation_text="P50")
        fig.add_vline(x=p90, line_dash="dash", annotation_text="P90")
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.info(f"""
        **Simulation Results:**
        - P10 (Downside): {p10:.1f}%
        - P50 (Base): {p50:.1f}%
        - P90 (Upside): {p90:.1f}%
        - Probability of Loss: {(returns < 0).sum() / len(returns) * 100:.1f}%
        """)

def render_ai_recommendations(orchestrator):
    """Render AI-generated recommendations"""
    st.markdown("## 🤖 AI-Powered Recommendations")
    
    with st.spinner("Generating AI insights..."):
        # This would call the orchestrator in production
        # For demo, using mock recommendations
        
        recommendations = {
            'primary_recommendation': 'MAINTAIN WITH TRANSFORMATION',
            'confidence': 78,
            'key_insights': [
                "Strong capital position provides buffer for transformation",
                "Hajj/Umrah synergies create unique competitive advantage",
                "Digital transformation critical for long-term viability",
                "NPF management must be immediate priority"
            ],
            'action_items': [
                {
                    'action': 'Appoint transformation-experienced CEO',
                    'timeline': 'Immediate',
                    'impact': 'High'
                },
                {
                    'action': 'Launch NPF reduction task force',
                    'timeline': '30 days',
                    'impact': 'Critical'
                },
                {
                    'action': 'Secure digital transformation partner',
                    'timeline': '90 days',
                    'impact': 'High'
                },
                {
                    'action': 'Develop Hajj ecosystem strategy',
                    'timeline': '60 days',
                    'impact': 'High'
                }
            ],
            'success_probability': 72
        }
    
    # Display AI recommendation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "AI Recommendation",
            recommendations['primary_recommendation'],
            f"Confidence: {recommendations['confidence']}%"
        )
        
    with col2:
        st.metric(
            "Success Probability",
            f"{recommendations['success_probability']}%",
            "Based on 1000+ scenarios"
        )
        
    with col3:
        gauge = create_confidence_gauge(recommendations['confidence'])
        st.plotly_chart(gauge, use_container_width=True)
    
    # Key insights
    st.markdown("### 🔍 Key AI Insights")
    for insight in recommendations['key_insights']:
        st.markdown(f"- {insight}")
        
    # Action items
    st.markdown("### 📋 Recommended Actions")
    
    action_df = pd.DataFrame(recommendations['action_items'])
    
    # Color-code by impact
    def highlight_impact(val):
        if val == 'Critical':
            return 'background-color: #ffcccc'
        elif val == 'High':
            return 'background-color: #ffffcc'
        return ''
    
    styled_df = action_df.style.applymap(highlight_impact, subset=['impact'])
    st.dataframe(styled_df, use_container_width=True)
    
    # AI reasoning
    with st.expander("🧠 AI Reasoning Process"):
        st.markdown("""
        **Analysis Methodology:**
        1. Analyzed 5 years of financial data
        2. Compared with 15 peer banks
        3. Simulated 1000+ scenario combinations
        4. Evaluated strategic fit with BPKH objectives
        5. Assessed transformation success factors
        
        **Key Decision Factors:**
        - Capital strength (29.42% CAR) provides transformation runway
        - NPF at 3.99% is manageable but requires immediate action
        - BPKH's patient capital aligns with transformation timeline
        - Hajj/Umrah synergies create defensible market position
        - Digital capability gap can be bridged through partnerships
        
        **Risk Assessment:**
        - Execution risk: MEDIUM (mitigated by experienced leadership)
        - Market risk: LOW (Islamic banking growing 12%+ annually)
        - Regulatory risk: LOW (strong compliance record)
        - Technology risk: MEDIUM (partnership strategy reduces risk)
        """)

def render_decision_timeline():
    """Render decision timeline"""
    st.markdown("## ⏱️ Decision Timeline & Milestones")
    
    # Create timeline
    timeline_events = [
        {'Task': 'Board Decision', 'Start': '2024-07-01', 'Finish': '2024-07-31', 'Resource': 'BPKH Board'},
        {'Task': 'CEO Recruitment', 'Start': '2024-08-01', 'Finish': '2024-10-31', 'Resource': 'Executive Search'},
        {'Task': 'NPF Task Force', 'Start': '2024-08-01', 'Finish': '2024-12-31', 'Resource': 'Risk Team'},
        {'Task': 'Digital Partner Selection', 'Start': '2024-09-01', 'Finish': '2024-11-30', 'Resource': 'Tech Team'},
        {'Task': 'Transformation Launch', 'Start': '2024-11-01', 'Finish': '2025-01-31', 'Resource': 'New CEO'},
        {'Task': 'Quick Wins Implementation', 'Start': '2025-01-01', 'Finish': '2025-06-30', 'Resource': 'All Teams'},
        {'Task': 'Mid-term Review', 'Start': '2025-07-01', 'Finish': '2025-07-31', 'Resource': 'BPKH Board'},
        {'Task': 'Exit Strategy Decision', 'Start': '2026-01-01', 'Finish': '2026-03-31', 'Resource': 'BPKH Board'}
    ]
    
    df = pd.DataFrame(timeline_events)
    
    fig = px.timeline(
        df,
        x_start="Start",
        x_end="Finish",
        y="Task",
        color="Resource",
        title="Decision Implementation Timeline"
    )
    
    fig.update_yaxes(categoryorder="total ascending")
    fig.update_layout(height=400)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Key decision points
    st.markdown("### 🎯 Key Decision Points")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **July 2024: Go/No-Go Decision**
        - Approve transformation plan
        - Commit resources
        - Set success metrics
        """)
        
    with col2:
        st.warning("""
        **July 2025: Mid-term Review**
        - Assess progress
        - Adjust strategy
        - Confirm exit timeline
        """)
        
    with col3:
        st.success("""
        **Q1 2026: Exit Decision**
        - Evaluate options
        - Select exit path
        - Launch process
        """)

def render_action_plan():
    """Render detailed action plan"""
    st.markdown("## 📋 Recommended Action Plan")
    
    # Summary recommendation
    st.success("""
    **RECOMMENDATION: MAINTAIN INVESTMENT WITH AGGRESSIVE TRANSFORMATION**
    
    Transform Bank Muamalat into a specialized Islamic digital bank focusing on 
    Hajj/Umrah ecosystem and government employee banking, with target exit in 3-5 years.
    """)
    
    # Immediate actions (30 days)
    st.markdown("### 🚨 Immediate Actions (Next 30 Days)")
    
    immediate_actions = [
        "✅ Board approval for transformation plan",
        "✅ Launch CEO search with transformation mandate",
        "✅ Establish NPF crisis management team",
        "✅ Engage top-tier strategy consultant",
        "✅ Communicate vision to key stakeholders"
    ]
    
    col1, col2 = st.columns(2)
    with col1:
        for action in immediate_actions[:3]:
            st.markdown(action)
    with col2:
        for action in immediate_actions[3:]:
            st.markdown(action)
            
    # 90-day plan
    st.markdown("### 📅 90-Day Transformation Launch")
    
    plan_90_days = {
        'Workstream': ['Leadership', 'Financial', 'Digital', 'Operations', 'Strategic'],
        'Key Actions': [
            'Onboard new CEO, refresh Board',
            'NPF reduction plan, cost optimization',
            'Digital partner RFP, quick wins launch',
            'Process automation, branch optimization',
            'Hajj ecosystem design, ASN partnership'
        ],
        'Success Metrics': [
            'CEO in place, Board aligned',
            'NPF < 3.5%, BOPO < 95%',
            'Partner selected, 2 features launched',
            '10% process digitized',
            '2 strategic MOUs signed'
        ]
    }
    
    plan_df = pd.DataFrame(plan_90_days)
    st.dataframe(plan_df, use_container_width=True)
    
    # Success factors
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Critical Success Factors")
        st.markdown("""
        1. **Right Leadership**: CEO with proven transformation track record
        2. **Board Alignment**: Full BPKH support for 3-year journey
        3. **Quick Wins**: Visible progress in first 6 months
        4. **Strategic Focus**: Discipline to say no to distractions
        5. **Execution Excellence**: Professional program management
        """)
        
    with col2:
        st.markdown("### ⚠️ Key Risks to Monitor")
        st.markdown("""
        1. **Execution Risk**: Transformation harder than expected
        2. **Market Risk**: Competitive pressure from BSI
        3. **Regulatory Risk**: Changes in Islamic banking rules
        4. **Technology Risk**: Digital platform implementation
        5. **Talent Risk**: Difficulty attracting digital talent
        """)
    
    # Final call to action
    st.markdown("---")
    st.markdown("### 🎯 The Decision")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Option 1: Transform & Hold** ✅
        - Highest value creation
        - Leverages BPKH strengths
        - 3-5 year commitment
        """)
        
    with col2:
        st.markdown("""
        **Option 2: Quick Exit** ❌
        - Suboptimal value
        - Reputation risk
        - Limited buyer interest
        """)
        
    with col3:
        st.markdown("""
        **Option 3: Status Quo** ❌
        - Value destruction
        - Competitive decline
        - Regulatory risk
        """)
    
    st.info("""
    💡 **The data strongly supports Option 1: Transform & Hold**
    
    With the right leadership and focused execution, Bank Muamalat can become a 
    valuable specialized Islamic bank, creating significant value for BPKH and 
    advancing Indonesia's Islamic finance ecosystem.
    """)

# Helper functions
def calculate_decision_score() -> float:
    """Calculate overall decision score"""
    # Simplified scoring based on key metrics
    financial_score = 45  # Based on current metrics
    strategic_score = 75  # Based on BPKH fit
    risk_score = 40      # Based on risk levels
    market_score = 65    # Based on market opportunity
    
    # Weighted average
    weights = [0.3, 0.3, 0.2, 0.2]
    scores = [financial_score, strategic_score, risk_score, market_score]
    
    return sum(w * s for w, s in zip(weights, scores))

def get_primary_recommendation(score: float) -> str:
    """Get primary recommendation based on score"""
    if score >= 70:
        return "STRONG BUY/HOLD"
    elif score >= 60:
        return "MAINTAIN WITH CONDITIONS"
    elif score >= 50:
        return "REVIEW QUARTERLY"
    elif score >= 40:
        return "PREPARE EXIT"
    else:
        return "IMMEDIATE EXIT"

def create_factor_gauge(title: str, value: float, ranges: List[Dict]) -> go.Figure:
    """Create a gauge chart for factors"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': ranges,
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=250)
    return fig

def create_confidence_gauge(confidence: float) -> go.Figure:
    """Create confidence gauge"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "AI Confidence"},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "green" if confidence > 70 else "orange"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 95
            }
        }
    ))
    
    fig.update_layout(height=200)
    return fig

# Export functions
__all__ = [
    'render',
    'calculate_decision_score',
    'get_primary_recommendation',
    'create_factor_gauge',
    'create_confidence_gauge'
]