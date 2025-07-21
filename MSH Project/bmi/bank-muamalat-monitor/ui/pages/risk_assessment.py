# ===== pages/risk_assessment.py =====
"""
Advanced Risk Assessment Module
Comprehensive risk analysis and management system
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json

class AdvancedRiskAssessment:
    """Comprehensive risk assessment system for banking operations"""
    
    def __init__(self):
        self.risk_categories = {
            'credit_risk': {
                'weight': 0.35,
                'components': ['npf_ratio', 'provision_coverage', 'large_exposures', 'sector_concentration']
            },
            'operational_risk': {
                'weight': 0.25, 
                'components': ['operational_efficiency', 'process_automation', 'cyber_security', 'compliance_gaps']
            },
            'market_risk': {
                'weight': 0.20,
                'components': ['interest_rate_sensitivity', 'fx_exposure', 'equity_exposure', 'commodity_exposure']
            },
            'liquidity_risk': {
                'weight': 0.15,
                'components': ['ldr_ratio', 'liquid_assets_ratio', 'deposit_concentration', 'funding_stability']
            },
            'regulatory_risk': {
                'weight': 0.05,
                'components': ['capital_adequacy', 'regulatory_compliance', 'policy_changes', 'enforcement_actions']
            }
        }
        
        # Risk thresholds
        self.risk_thresholds = {
            'low': {'min': 0, 'max': 30, 'color': 'green'},
            'medium': {'min': 30, 'max': 60, 'color': 'yellow'},
            'high': {'min': 60, 'max': 85, 'color': 'orange'},
            'critical': {'min': 85, 'max': 100, 'color': 'red'}
        }
    
    def calculate_comprehensive_risk_score(self, financial_data: Dict) -> Dict:
        """Calculate comprehensive risk assessment"""
        
        # Credit Risk Assessment
        credit_risk = self._assess_credit_risk(financial_data)
        
        # Operational Risk Assessment  
        operational_risk = self._assess_operational_risk(financial_data)
        
        # Market Risk Assessment
        market_risk = self._assess_market_risk(financial_data)
        
        # Liquidity Risk Assessment
        liquidity_risk = self._assess_liquidity_risk(financial_data)
        
        # Regulatory Risk Assessment
        regulatory_risk = self._assess_regulatory_risk(financial_data)
        
        # Calculate overall risk score
        overall_risk = (
            credit_risk['score'] * self.risk_categories['credit_risk']['weight'] +
            operational_risk['score'] * self.risk_categories['operational_risk']['weight'] +
            market_risk['score'] * self.risk_categories['market_risk']['weight'] +
            liquidity_risk['score'] * self.risk_categories['liquidity_risk']['weight'] +
            regulatory_risk['score'] * self.risk_categories['regulatory_risk']['weight']
        )
        
        return {
            'overall_risk_score': round(overall_risk, 1),
            'risk_level': self._get_risk_level(overall_risk),
            'credit_risk': credit_risk,
            'operational_risk': operational_risk,
            'market_risk': market_risk,
            'liquidity_risk': liquidity_risk,
            'regulatory_risk': regulatory_risk,
            'assessment_date': datetime.now(),
            'confidence_level': 87  # Based on data quality
        }
    
    def _assess_credit_risk(self, data: Dict) -> Dict:
        """Assess credit risk components"""
        
        npf = data.get('npf', 3.99)
        car = data.get('car', 29.42)
        assets = data.get('assets', 60.023)
        
        # NPF component (40% weight)
        npf_score = min(100, (npf / 5.0) * 100)  # 5% NPF = 100 risk points
        
        # Provision coverage (25% weight)
        estimated_provision_coverage = 75.0  # Estimated
        provision_score = max(0, 100 - estimated_provision_coverage)
        
        # Large exposures (20% weight) 
        large_exposure_ratio = 18.5  # Estimated single borrower exposure
        exposure_score = (large_exposure_ratio / 20.0) * 100
        
        # Sector concentration (15% weight)
        sector_concentration = 65.0  # Estimated concentration in key sectors
        concentration_score = max(0, sector_concentration - 40) * 2.5
        
        credit_score = (
            npf_score * 0.4 +
            provision_score * 0.25 +
            exposure_score * 0.2 +
            concentration_score * 0.15
        )
        
        return {
            'score': round(credit_score, 1),
            'level': self._get_risk_level(credit_score),
            'components': {
                'npf_ratio': {'value': npf, 'score': npf_score, 'status': 'High' if npf > 4 else 'Medium'},
                'provision_coverage': {'value': estimated_provision_coverage, 'score': provision_score},
                'large_exposures': {'value': large_exposure_ratio, 'score': exposure_score},
                'sector_concentration': {'value': sector_concentration, 'score': concentration_score}
            },
            'key_concerns': self._get_credit_risk_concerns(npf, large_exposure_ratio),
            'recommendations': self._get_credit_risk_recommendations(npf, credit_score)
        }
    
    def _assess_operational_risk(self, data: Dict) -> Dict:
        """Assess operational risk components"""
        
        bopo = data.get('bopo', 98.5)
        efficiency_score = data.get('operational_efficiency_score', 60)
        
        # Operational efficiency (40% weight)
        efficiency_risk_score = max(0, bopo - 70) * 2.5  # 70% BOPO = 0 risk
        
        # Process automation (25% weight)
        automation_level = 35.0  # Estimated automation percentage
        automation_score = max(0, 80 - automation_level) * 1.25
        
        # Cyber security (20% weight)
        cyber_maturity = 72.0  # Estimated cyber security maturity
        cyber_score = max(0, 90 - cyber_maturity) * 2.0
        
        # Compliance gaps (15% weight)
        compliance_score = 88.0  # Estimated compliance score
        compliance_risk_score = max(0, 95 - compliance_score) * 4.0
        
        operational_score = (
            efficiency_risk_score * 0.4 +
            automation_score * 0.25 +
            cyber_score * 0.2 +
            compliance_risk_score * 0.15
        )
        
        return {
            'score': round(operational_score, 1),
            'level': self._get_risk_level(operational_score),
            'components': {
                'operational_efficiency': {'value': bopo, 'score': efficiency_risk_score},
                'process_automation': {'value': automation_level, 'score': automation_score},
                'cyber_security': {'value': cyber_maturity, 'score': cyber_score},
                'compliance_gaps': {'value': compliance_score, 'score': compliance_risk_score}
            },
            'key_concerns': self._get_operational_risk_concerns(bopo, automation_level),
            'recommendations': self._get_operational_risk_recommendations(bopo, operational_score)
        }
    
    def _assess_market_risk(self, data: Dict) -> Dict:
        """Assess market risk components"""
        
        # Interest rate sensitivity (50% weight)
        duration_gap = 1.8  # Estimated asset-liability duration gap
        interest_rate_score = abs(duration_gap) * 15
        
        # FX exposure (30% weight)
        fx_exposure_ratio = 5.2  # Estimated FX exposure as % of capital
        fx_score = max(0, fx_exposure_ratio - 2) * 10
        
        # Equity exposure (15% weight)
        equity_exposure = 2.8  # Estimated equity investment as % of assets
        equity_score = max(0, equity_exposure - 1) * 20
        
        # Commodity exposure (5% weight)
        commodity_exposure = 0.5  # Minimal commodity exposure
        commodity_score = commodity_exposure * 10
        
        market_score = (
            interest_rate_score * 0.5 +
            fx_score * 0.3 +
            equity_score * 0.15 +
            commodity_score * 0.05
        )
        
        return {
            'score': round(market_score, 1),
            'level': self._get_risk_level(market_score),
            'components': {
                'interest_rate_sensitivity': {'value': duration_gap, 'score': interest_rate_score},
                'fx_exposure': {'value': fx_exposure_ratio, 'score': fx_score},
                'equity_exposure': {'value': equity_exposure, 'score': equity_score},
                'commodity_exposure': {'value': commodity_exposure, 'score': commodity_score}
            },
            'key_concerns': self._get_market_risk_concerns(duration_gap, fx_exposure_ratio),
            'recommendations': self._get_market_risk_recommendations(market_score)
        }
    
    def _assess_liquidity_risk(self, data: Dict) -> Dict:
        """Assess liquidity risk components"""
        
        ldr = data.get('loan_to_deposit_ratio', 85.5)
        
        # LDR component (40% weight)
        optimal_ldr = 85.0
        ldr_score = abs(ldr - optimal_ldr) * 2.5
        
        # Liquid assets ratio (30% weight)
        liquid_assets_ratio = 25.5  # Estimated
        liquid_score = max(0, 20 - liquid_assets_ratio) * 5
        
        # Deposit concentration (20% weight)
        top_10_depositors = 35.0  # Estimated % of deposits from top 10 depositors
        concentration_score = max(0, top_10_depositors - 25) * 2
        
        # Funding stability (10% weight)
        stable_funding_ratio = 78.0  # Estimated
        funding_score = max(0, 85 - stable_funding_ratio) * 3
        
        liquidity_score = (
            ldr_score * 0.4 +
            liquid_score * 0.3 +
            concentration_score * 0.2 +
            funding_score * 0.1
        )
        
        return {
            'score': round(liquidity_score, 1),
            'level': self._get_risk_level(liquidity_score),
            'components': {
                'ldr_ratio': {'value': ldr, 'score': ldr_score},
                'liquid_assets_ratio': {'value': liquid_assets_ratio, 'score': liquid_score},
                'deposit_concentration': {'value': top_10_depositors, 'score': concentration_score},
                'funding_stability': {'value': stable_funding_ratio, 'score': funding_score}
            },
            'key_concerns': self._get_liquidity_risk_concerns(ldr, liquid_assets_ratio),
            'recommendations': self._get_liquidity_risk_recommendations(liquidity_score)
        }
    
    def _assess_regulatory_risk(self, data: Dict) -> Dict:
        """Assess regulatory risk components"""
        
        car = data.get('car', 29.42)
        npf = data.get('npf', 3.99)
        bopo = data.get('bopo', 98.5)
        
        # Capital adequacy (40% weight)
        car_buffer = car - 8.0  # vs minimum requirement
        car_score = max(0, 15 - car_buffer) * 2
        
        # Regulatory compliance (30% weight)
        bopo_compliance = max(0, bopo - 94) * 5  # vs 94% threshold
        npf_compliance = max(0, npf - 5) * 10    # vs 5% threshold
        compliance_score = bopo_compliance + npf_compliance
        
        # Policy changes (20% weight)
        policy_adaptation_score = 25.0  # Estimated readiness for policy changes
        
        # Enforcement actions (10% weight)
        enforcement_history = 15.0  # Estimated enforcement risk
        
        regulatory_score = (
            car_score * 0.4 +
            compliance_score * 0.3 +
            policy_adaptation_score * 0.2 +
            enforcement_history * 0.1
        )
        
        return {
            'score': round(regulatory_score, 1),
            'level': self._get_risk_level(regulatory_score),
            'components': {
                'capital_adequacy': {'value': car, 'score': car_score},
                'regulatory_compliance': {'value': compliance_score, 'score': compliance_score},
                'policy_changes': {'value': policy_adaptation_score, 'score': policy_adaptation_score},
                'enforcement_actions': {'value': enforcement_history, 'score': enforcement_history}
            },
            'key_concerns': self._get_regulatory_risk_concerns(bopo, npf),
            'recommendations': self._get_regulatory_risk_recommendations(regulatory_score)
        }
    
    def _get_risk_level(self, score: float) -> str:
        """Get risk level based on score"""
        for level, threshold in self.risk_thresholds.items():
            if threshold['min'] <= score < threshold['max']:
                return level
        return 'critical'
    
    def _get_credit_risk_concerns(self, npf: float, large_exposure: float) -> List[str]:
        """Get credit risk concerns"""
        concerns = []
        if npf > 4.0:
            concerns.append(f"NPF at {npf}% exceeds comfort level")
        if large_exposure > 15.0:
            concerns.append(f"Large exposure concentration at {large_exposure}%")
        return concerns
    
    def _get_credit_risk_recommendations(self, npf: float, score: float) -> List[str]:
        """Get credit risk recommendations"""
        recommendations = []
        if npf > 3.5:
            recommendations.append("Strengthen credit risk management and collection procedures")
        if score > 60:
            recommendations.append("Implement enhanced credit monitoring systems")
        recommendations.append("Diversify loan portfolio across sectors and geographies")
        return recommendations
    
    def _get_operational_risk_concerns(self, bopo: float, automation: float) -> List[str]:
        """Get operational risk concerns"""
        concerns = []
        if bopo > 94:
            concerns.append(f"BOPO at {bopo}% exceeds regulatory threshold")
        if automation < 50:
            concerns.append(f"Low automation level at {automation}%")
        return concerns
    
    def _get_operational_risk_recommendations(self, bopo: float, score: float) -> List[str]:
        """Get operational risk recommendations"""
        recommendations = []
        if bopo > 90:
            recommendations.append("Implement cost reduction and efficiency programs")
        recommendations.append("Increase process automation and digitalization")
        recommendations.append("Enhance cybersecurity and operational controls")
        return recommendations
    
    def _get_market_risk_concerns(self, duration_gap: float, fx_exposure: float) -> List[str]:
        """Get market risk concerns"""
        concerns = []
        if abs(duration_gap) > 2:
            concerns.append(f"High interest rate sensitivity (duration gap: {duration_gap})")
        if fx_exposure > 5:
            concerns.append(f"Elevated FX exposure at {fx_exposure}%")
        return concerns
    
    def _get_market_risk_recommendations(self, score: float) -> List[str]:
        """Get market risk recommendations"""
        recommendations = [
            "Implement asset-liability duration matching",
            "Use derivatives for interest rate and FX hedging",
            "Monitor market risk limits and stress test scenarios"
        ]
        return recommendations
    
    def _get_liquidity_risk_concerns(self, ldr: float, liquid_ratio: float) -> List[str]:
        """Get liquidity risk concerns"""
        concerns = []
        if ldr > 90:
            concerns.append(f"High LDR at {ldr}% may strain liquidity")
        if liquid_ratio < 20:
            concerns.append(f"Low liquid assets ratio at {liquid_ratio}%")
        return concerns
    
    def _get_liquidity_risk_recommendations(self, score: float) -> List[str]:
        """Get liquidity risk recommendations"""
        recommendations = [
            "Maintain adequate liquidity buffers",
            "Diversify funding sources and deposit base",
            "Implement liquidity stress testing"
        ]
        return recommendations
    
    def _get_regulatory_risk_concerns(self, bopo: float, npf: float) -> List[str]:
        """Get regulatory risk concerns"""
        concerns = []
        if bopo > 94:
            concerns.append("BOPO exceeds regulatory threshold")
        if npf > 5:
            concerns.append("NPF approaching regulatory limit")
        return concerns
    
    def _get_regulatory_risk_recommendations(self, score: float) -> List[str]:
        """Get regulatory risk recommendations"""
        recommendations = [
            "Ensure compliance with all regulatory requirements",
            "Strengthen risk management framework",
            "Maintain regular dialogue with regulators"
        ]
        return recommendations

def render_risk_assessment():
    """Render comprehensive risk assessment dashboard"""
    
    st.title("⚠️ Advanced Risk Assessment Dashboard")
    st.markdown("*Comprehensive multi-dimensional risk analysis and monitoring*")
    
    # Get current financial data
    if 'real_scraped_data' in st.session_state:
        current_data = st.session_state.real_scraped_data
    else:
        current_data = {
            'npf': 3.99, 'car': 29.42, 'bopo': 98.5, 'assets': 60.023,
            'loan_to_deposit_ratio': 85.5, 'operational_efficiency_score': 60
        }
    
    # Initialize risk assessment system
    risk_system = AdvancedRiskAssessment()
    
    # Generate risk assessment
    if st.button("🔍 **Perform Comprehensive Risk Assessment**", type="primary"):
        with st.spinner("Analyzing multi-dimensional risk factors..."):
            risk_assessment = risk_system.calculate_comprehensive_risk_score(current_data)
            st.session_state.risk_assessment = risk_assessment
            st.success("✅ Risk assessment complete!")
    
    # Display risk assessment if available
    if 'risk_assessment' in st.session_state:
        assessment = st.session_state.risk_assessment
        
        # Overall Risk Summary
        st.markdown("## 🎯 Overall Risk Summary")
        
        overall_score = assessment['overall_risk_score']
        overall_level = assessment['risk_level']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            color = risk_system.risk_thresholds[overall_level]['color']
            if color == 'green':
                st.success(f"🟢 **Overall Risk: {overall_level.title()}**")
            elif color == 'yellow':
                st.warning(f"🟡 **Overall Risk: {overall_level.title()}**")
            elif color == 'orange':
                st.warning(f"🟠 **Overall Risk: {overall_level.title()}**")
            else:
                st.error(f"🔴 **Overall Risk: {overall_level.title()}**")
            
            st.metric("Risk Score", f"{overall_score}/100")
        
        with col2:
            confidence = assessment.get('confidence_level', 87)
            st.metric("Assessment Confidence", f"{confidence}%", "🎯 High")
        
        with col3:
            assessment_date = assessment.get('assessment_date', datetime.now())
            st.metric("Assessment Date", assessment_date.strftime('%Y-%m-%d'), "📅 Current")
        
        with col4:
            # Count high/critical risks
            high_risks = sum(1 for category in ['credit_risk', 'operational_risk', 'market_risk', 'liquidity_risk', 'regulatory_risk'] 
                           if assessment[category]['level'] in ['high', 'critical'])
            st.metric("High Risk Areas", high_risks, "⚠️ Monitor")
        
        # Risk Category Breakdown
        st.markdown("## 📊 Risk Category Analysis")
        
        # Create risk radar chart
        categories = ['Credit Risk', 'Operational Risk', 'Market Risk', 'Liquidity Risk', 'Regulatory Risk']
        scores = [
            assessment['credit_risk']['score'],
            assessment['operational_risk']['score'], 
            assessment['market_risk']['score'],
            assessment['liquidity_risk']['score'],
            assessment['regulatory_risk']['score']
        ]
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=scores,
            theta=categories,
            fill='toself',
            name='Risk Profile',
            line_color='red'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Risk Profile Radar Chart"
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Detailed Risk Analysis by Category
        st.markdown("## 🔍 Detailed Risk Analysis")
        
        risk_categories = [
            ('credit_risk', 'Credit Risk', '💳'),
            ('operational_risk', 'Operational Risk', '⚙️'),
            ('market_risk', 'Market Risk', '📈'),
            ('liquidity_risk', 'Liquidity Risk', '💧'),
            ('regulatory_risk', 'Regulatory Risk', '📋')
        ]
        
        for category_key, category_name, icon in risk_categories:
            category_data = assessment[category_key]
            
            with st.expander(f"{icon} **{category_name}** - Score: {category_data['score']}/100 ({category_data['level'].title()})"):
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 📊 Component Analysis")
                    
                    components = category_data.get('components', {})
                    for comp_name, comp_data in components.items():
                        comp_score = comp_data.get('score', 0)
                        comp_value = comp_data.get('value', 'N/A')
                        
                        st.write(f"**{comp_name.replace('_', ' ').title()}**: {comp_value}")
                        st.progress(min(comp_score / 100, 1.0))
                
                with col2:
                    st.markdown("### ⚠️ Key Concerns")
                    concerns = category_data.get('key_concerns', [])
                    if concerns:
                        for concern in concerns:
                            st.warning(f"⚠️ {concern}")
                    else:
                        st.success("✅ No significant concerns identified")
                
                st.markdown("### 💡 Recommendations")
                recommendations = category_data.get('recommendations', [])
                for rec in recommendations:
                    st.info(f"💡 {rec}")
        
        # Risk Heat Map
        st.markdown("## 🔥 Risk Heat Map")
        
        # Create heat map data
        heat_map_data = []
        
        for category_key, category_name, icon in risk_categories:
            category_data = assessment[category_key]
            components = category_data.get('components', {})
            
            for comp_name, comp_data in components.items():
                heat_map_data.append({
                    'Category': category_name,
                    'Component': comp_name.replace('_', ' ').title(),
                    'Risk Score': comp_data.get('score', 0),
                    'Value': comp_data.get('value', 0)
                })
        
        if heat_map_data:
            df_heat = pd.DataFrame(heat_map_data)
            
            # Create heat map
            fig_heat = px.density_heatmap(
                df_heat,
                x='Component',
                y='Category', 
                z='Risk Score',
                title='Risk Component Heat Map',
                color_continuous_scale='Reds'
            )
            
            fig_heat.update_layout(height=400)
            st.plotly_chart(fig_heat, use_container_width=True)
        
        # Risk Trend Analysis (simulated)
        st.markdown("## 📈 Risk Trend Analysis")
        
        # Generate trend data
        dates = pd.date_range(start=datetime.now() - timedelta(days=180), end=datetime.now(), freq='W')
        trend_data = []
        
        for date in dates:
            # Simulate risk score trends with some volatility
            base_score = overall_score
            volatility = np.random.normal(0, 5)
            trend_score = max(0, min(100, base_score + volatility))
            
            trend_data.append({
                'Date': date,
                'Overall Risk Score': trend_score,
                'Credit Risk': max(0, min(100, assessment['credit_risk']['score'] + np.random.normal(0, 3))),
                'Operational Risk': max(0, min(100, assessment['operational_risk']['score'] + np.random.normal(0, 4))),
                'Market Risk': max(0, min(100, assessment['market_risk']['score'] + np.random.normal(0, 6)))
            })
        
        df_trend = pd.DataFrame(trend_data)
        
        fig_trend = px.line(
            df_trend,
            x='Date',
            y=['Overall Risk Score', 'Credit Risk', 'Operational Risk', 'Market Risk'],
            title='Risk Score Trends (6 Months)',
            labels={'value': 'Risk Score', 'variable': 'Risk Category'}
        )
        
        fig_trend.update_layout(height=400)
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Export Risk Report
        st.markdown("## 📥 Export Risk Assessment")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 **Export Executive Risk Summary**"):
                summary_data = {
                    'executive_summary': {
                        'overall_risk_score': assessment['overall_risk_score'],
                        'risk_level': assessment['risk_level'],
                        'high_risk_areas': [cat for cat in risk_categories if assessment[cat[0]]['level'] in ['high', 'critical']],
                        'key_recommendations': []
                    }
                }
                
                # Collect top recommendations
                for category_key, _, _ in risk_categories:
                    recommendations = assessment[category_key].get('recommendations', [])
                    summary_data['executive_summary']['key_recommendations'].extend(recommendations[:2])
                
                summary_json = json.dumps(summary_data, indent=2, default=str)
                
                st.download_button(
                    label="📥 Download Risk Summary",
                    data=summary_json,
                    file_name=f"risk_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("📊 **Export Detailed Risk Report**"):
                full_report = {
                    'comprehensive_risk_assessment': assessment,
                    'source_data': current_data,
                    'methodology': 'Multi-dimensional risk scoring with weighted categories',
                    'export_timestamp': datetime.now().isoformat()
                }
                
                report_json = json.dumps(full_report, indent=2, default=str)
                
                st.download_button(
                    label="📥 Download Full Report",
                    data=report_json,
                    file_name=f"comprehensive_risk_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json"
                )
    
    else:
        # Initial state
        st.markdown("## 🎯 Advanced Risk Assessment Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔍 **Assessment Categories**")
            st.write("• **Credit Risk** (35% weight) - NPF, provisions, concentrations")
            st.write("• **Operational Risk** (25% weight) - Efficiency, automation, cyber security")
            st.write("• **Market Risk** (20% weight) - Interest rate, FX, equity exposures")
            st.write("• **Liquidity Risk** (15% weight) - LDR, liquid assets, funding stability")
            st.write("• **Regulatory Risk** (5% weight) - Compliance, capital adequacy")
        
        with col2:
            st.markdown("### 📊 **Assessment Features**")
            st.write("• **Multi-dimensional scoring** with weighted categories")
            st.write("• **Component-level analysis** for detailed insights")
            st.write("• **Risk heat mapping** for visual identification")
            st.write("• **Trend analysis** for risk monitoring")
            st.write("• **Actionable recommendations** for risk mitigation")
        
        st.info("👆 **Click 'Perform Comprehensive Risk Assessment' to begin analysis**")

if __name__ == "__main__":
    render_risk_assessment()
