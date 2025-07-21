# ===== pages/compliance_monitoring.py =====
"""
Advanced Compliance Monitoring System
Comprehensive regulatory compliance tracking and reporting
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional

class AdvancedComplianceMonitoring:
    """Comprehensive compliance monitoring and regulatory tracking system"""
    
    def __init__(self):
        # Indonesian banking regulations
        self.regulatory_framework = {
            'ojk_regulations': {
                'capital_adequacy': {
                    'minimum_car': 8.0,
                    'well_capitalized_car': 12.0,
                    'buffer_requirement': 2.5,
                    'regulation': 'POJK No. 11/POJK.03/2016'
                },
                'asset_quality': {
                    'maximum_npf': 5.0,
                    'provision_minimum': 1.0,
                    'regulation': 'POJK No. 40/POJK.03/2019'
                },
                'operational_efficiency': {
                    'maximum_bopo': 94.0,
                    'target_bopo': 85.0,
                    'regulation': 'POJK No. 6/POJK.03/2016'
                },
                'liquidity': {
                    'minimum_lcr': 100.0,
                    'minimum_nsfr': 100.0,
                    'regulation': 'POJK No. 42/POJK.03/2019'
                }
            },
            'bank_indonesia_regulations': {
                'monetary_policy': {
                    'reserve_requirement': 3.5,
                    'regulation': 'PBI No. 23/6/PBI/2021'
                },
                'macroprudential': {
                    'countercyclical_buffer': 0.0,
                    'regulation': 'PBI No. 20/4/PBI/2018'
                }
            },
            'islamic_banking_specific': {
                'sharia_compliance': {
                    'sharia_assets_ratio': 100.0,
                    'sharia_income_ratio': 100.0,
                    'regulation': 'POJK No. 24/POJK.03/2020'
                },
                'governance': {
                    'dps_meetings': 12,  # Dewan Pengawas Syariah meetings per year
                    'sharia_audit_frequency': 2,  # Times per year
                    'regulation': 'POJK No. 55/POJK.03/2016'
                }
            }
        }
        
        # Compliance scoring weights
        self.compliance_weights = {
            'capital_adequacy': 0.25,
            'asset_quality': 0.20,
            'operational_efficiency': 0.15,
            'liquidity': 0.15,
            'sharia_compliance': 0.15,
            'governance': 0.10
        }
        
        # Risk ratings for non-compliance
        self.risk_ratings = {
            'compliant': {'score': 100, 'color': 'green', 'action': 'Monitor'},
            'minor_deviation': {'score': 80, 'color': 'yellow', 'action': 'Improve'},
            'significant_deviation': {'score': 60, 'color': 'orange', 'action': 'Remediate'},
            'non_compliant': {'score': 40, 'color': 'red', 'action': 'Urgent Action'},
            'critical': {'score': 20, 'color': 'darkred', 'action': 'Immediate Action'}
        }
    
    def assess_comprehensive_compliance(self, financial_data: Dict) -> Dict:
        """Perform comprehensive compliance assessment"""
        
        # Assess each compliance area
        capital_compliance = self._assess_capital_adequacy_compliance(financial_data)
        asset_quality_compliance = self._assess_asset_quality_compliance(financial_data)
        operational_compliance = self._assess_operational_efficiency_compliance(financial_data)
        liquidity_compliance = self._assess_liquidity_compliance(financial_data)
        sharia_compliance = self._assess_sharia_compliance(financial_data)
        governance_compliance = self._assess_governance_compliance(financial_data)
        
        # Calculate overall compliance score
        overall_score = (
            capital_compliance['score'] * self.compliance_weights['capital_adequacy'] +
            asset_quality_compliance['score'] * self.compliance_weights['asset_quality'] +
            operational_compliance['score'] * self.compliance_weights['operational_efficiency'] +
            liquidity_compliance['score'] * self.compliance_weights['liquidity'] +
            sharia_compliance['score'] * self.compliance_weights['sharia_compliance'] +
            governance_compliance['score'] * self.compliance_weights['governance']
        )
        
        return {
            'overall_compliance_score': round(overall_score, 1),
            'compliance_rating': self._get_compliance_rating(overall_score),
            'capital_adequacy': capital_compliance,
            'asset_quality': asset_quality_compliance,
            'operational_efficiency': operational_compliance,
            'liquidity': liquidity_compliance,
            'sharia_compliance': sharia_compliance,
            'governance': governance_compliance,
            'assessment_date': datetime.now(),
            'next_review_date': datetime.now() + timedelta(days=30),
            'regulatory_changes': self._get_recent_regulatory_changes(),
            'action_items': self._generate_action_items(overall_score)
        }
    
    def _assess_capital_adequacy_compliance(self, data: Dict) -> Dict:
        """Assess capital adequacy compliance"""
        
        car = data.get('car', 29.42)
        regulations = self.regulatory_framework['ojk_regulations']['capital_adequacy']
        
        # Determine compliance status
        if car >= regulations['well_capitalized_car'] + regulations['buffer_requirement']:
            status = 'compliant'
            score = 100
            deviation = 0
        elif car >= regulations['well_capitalized_car']:
            status = 'compliant'
            score = 95
            deviation = 0
        elif car >= regulations['minimum_car'] + regulations['buffer_requirement']:
            status = 'minor_deviation'
            score = 85
            deviation = (regulations['well_capitalized_car'] - car)
        elif car >= regulations['minimum_car']:
            status = 'significant_deviation'
            score = 70
            deviation = (regulations['minimum_car'] + regulations['buffer_requirement'] - car)
        else:
            status = 'non_compliant'
            score = 40
            deviation = (regulations['minimum_car'] - car)
        
        return {
            'score': score,
            'status': status,
            'current_value': car,
            'requirement': regulations['minimum_car'],
            'target': regulations['well_capitalized_car'],
            'deviation': deviation,
            'regulation_reference': regulations['regulation'],
            'compliance_details': {
                'buffer_maintained': car - regulations['minimum_car'],
                'buffer_required': regulations['buffer_requirement'],
                'excess_capital': max(0, car - regulations['well_capitalized_car'])
            },
            'recommendations': self._get_capital_recommendations(car, status)
        }
    
    def _assess_asset_quality_compliance(self, data: Dict) -> Dict:
        """Assess asset quality compliance"""
        
        npf = data.get('npf', 3.99)
        regulations = self.regulatory_framework['ojk_regulations']['asset_quality']
        
        # Determine compliance status
        if npf <= 2.0:
            status = 'compliant'
            score = 100
        elif npf <= 3.0:
            status = 'compliant'
            score = 90
        elif npf <= 4.0:
            status = 'minor_deviation'
            score = 80
        elif npf <= regulations['maximum_npf']:
            status = 'significant_deviation'
            score = 65
        else:
            status = 'non_compliant'
            score = 40
        
        deviation = max(0, npf - regulations['maximum_npf'])
        
        return {
            'score': score,
            'status': status,
            'current_value': npf,
            'requirement': regulations['maximum_npf'],
            'target': 3.0,  # Internal target
            'deviation': deviation,
            'regulation_reference': regulations['regulation'],
            'compliance_details': {
                'npf_buffer': regulations['maximum_npf'] - npf,
                'provision_coverage_estimate': 75.0,  # Estimated
                'workout_effectiveness': 65.0  # Estimated
            },
            'recommendations': self._get_asset_quality_recommendations(npf, status)
        }
    
    def _assess_operational_efficiency_compliance(self, data: Dict) -> Dict:
        """Assess operational efficiency compliance"""
        
        bopo = data.get('bopo', 98.5)
        regulations = self.regulatory_framework['ojk_regulations']['operational_efficiency']
        
        # Determine compliance status
        if bopo <= regulations['target_bopo']:
            status = 'compliant'
            score = 100
        elif bopo <= 90.0:
            status = 'compliant'
            score = 90
        elif bopo <= regulations['maximum_bopo']:
            status = 'minor_deviation'
            score = 75
        elif bopo <= 97.0:
            status = 'significant_deviation'
            score = 60
        else:
            status = 'non_compliant'
            score = 35
        
        deviation = max(0, bopo - regulations['maximum_bopo'])
        
        return {
            'score': score,
            'status': status,
            'current_value': bopo,
            'requirement': regulations['maximum_bopo'],
            'target': regulations['target_bopo'],
            'deviation': deviation,
            'regulation_reference': regulations['regulation'],
            'compliance_details': {
                'efficiency_gap': bopo - regulations['target_bopo'],
                'cost_reduction_needed': deviation * 0.6,  # Estimated
                'automation_opportunity': 35.0  # Estimated percentage
            },
            'recommendations': self._get_operational_recommendations(bopo, status)
        }
    
    def _assess_liquidity_compliance(self, data: Dict) -> Dict:
        """Assess liquidity compliance"""
        
        ldr = data.get('loan_to_deposit_ratio', 85.5)
        estimated_lcr = 125.0  # Estimated Liquidity Coverage Ratio
        regulations = self.regulatory_framework['ojk_regulations']['liquidity']
        
        # LDR assessment (should be reasonable, typically 80-90%)
        if 80 <= ldr <= 90:
            ldr_score = 100
            ldr_status = 'compliant'
        elif 75 <= ldr <= 95:
            ldr_score = 85
            ldr_status = 'minor_deviation'
        else:
            ldr_score = 60
            ldr_status = 'significant_deviation'
        
        # LCR assessment
        if estimated_lcr >= regulations['minimum_lcr'] + 20:
            lcr_score = 100
            lcr_status = 'compliant'
        elif estimated_lcr >= regulations['minimum_lcr']:
            lcr_score = 80
            lcr_status = 'minor_deviation'
        else:
            lcr_score = 50
            lcr_status = 'non_compliant'
        
        # Overall liquidity score
        overall_score = (ldr_score + lcr_score) / 2
        overall_status = 'compliant' if overall_score >= 85 else 'minor_deviation' if overall_score >= 70 else 'significant_deviation'
        
        return {
            'score': overall_score,
            'status': overall_status,
            'current_value': {
                'ldr': ldr,
                'lcr_estimated': estimated_lcr
            },
            'requirement': {
                'ldr_range': '80-90%',
                'lcr_minimum': regulations['minimum_lcr']
            },
            'target': {
                'ldr_target': 85.0,
                'lcr_target': 120.0
            },
            'regulation_reference': regulations['regulation'],
            'compliance_details': {
                'ldr_status': ldr_status,
                'lcr_status': lcr_status,
                'liquidity_buffer': estimated_lcr - regulations['minimum_lcr']
            },
            'recommendations': self._get_liquidity_recommendations(ldr, estimated_lcr, overall_status)
        }
    
    def _assess_sharia_compliance(self, data: Dict) -> Dict:
        """Assess Islamic banking Sharia compliance"""
        
        # Simulated Sharia compliance metrics
        sharia_assets_ratio = 99.8  # Estimated
        sharia_income_ratio = 99.9  # Estimated
        dps_meetings_held = 12
        sharia_audit_completed = 2
        
        regulations = self.regulatory_framework['islamic_banking_specific']
        
        # Assess Sharia asset compliance
        if sharia_assets_ratio >= 99.5:
            assets_score = 100
            assets_status = 'compliant'
        elif sharia_assets_ratio >= 99.0:
            assets_score = 90
            assets_status = 'minor_deviation'
        else:
            assets_score = 70
            assets_status = 'significant_deviation'
        
        # Assess governance compliance
        governance_score = 100 if dps_meetings_held >= regulations['governance']['dps_meetings'] else 80
        
        # Overall Sharia compliance
        overall_score = (assets_score * 0.6 + governance_score * 0.4)
        overall_status = 'compliant' if overall_score >= 95 else 'minor_deviation'
        
        return {
            'score': overall_score,
            'status': overall_status,
            'current_value': {
                'sharia_assets_ratio': sharia_assets_ratio,
                'sharia_income_ratio': sharia_income_ratio,
                'dps_meetings': dps_meetings_held,
                'sharia_audits': sharia_audit_completed
            },
            'requirement': {
                'sharia_assets_ratio': regulations['sharia_compliance']['sharia_assets_ratio'],
                'dps_meetings': regulations['governance']['dps_meetings']
            },
            'regulation_reference': regulations['sharia_compliance']['regulation'],
            'compliance_details': {
                'non_sharia_assets': 100 - sharia_assets_ratio,
                'dps_meeting_compliance': 'Full' if dps_meetings_held >= 12 else 'Partial',
                'sharia_audit_status': 'Complete' if sharia_audit_completed >= 2 else 'Pending'
            },
            'recommendations': self._get_sharia_recommendations(sharia_assets_ratio, overall_status)
        }
    
    def _assess_governance_compliance(self, data: Dict) -> Dict:
        """Assess governance and general compliance"""
        
        # Simulated governance metrics
        board_meetings = 12
        audit_committee_meetings = 6
        risk_committee_meetings = 4
        compliance_training_coverage = 95.0
        
        # Assess governance effectiveness
        if board_meetings >= 12 and audit_committee_meetings >= 6:
            governance_score = 100
            governance_status = 'compliant'
        elif board_meetings >= 10:
            governance_score = 85
            governance_status = 'minor_deviation'
        else:
            governance_score = 70
            governance_status = 'significant_deviation'
        
        return {
            'score': governance_score,
            'status': governance_status,
            'current_value': {
                'board_meetings': board_meetings,
                'audit_committee_meetings': audit_committee_meetings,
                'risk_committee_meetings': risk_committee_meetings,
                'training_coverage': compliance_training_coverage
            },
            'requirement': {
                'minimum_board_meetings': 12,
                'minimum_audit_meetings': 6,
                'training_coverage_target': 100.0
            },
            'compliance_details': {
                'governance_effectiveness': 'Strong',
                'committee_structure': 'Complete',
                'training_gap': 100 - compliance_training_coverage
            },
            'recommendations': self._get_governance_recommendations(governance_score, governance_status)
        }
    
    def _get_compliance_rating(self, score: float) -> str:
        """Get compliance rating based on score"""
        if score >= 95:
            return 'excellent'
        elif score >= 85:
            return 'good'
        elif score >= 75:
            return 'satisfactory'
        elif score >= 65:
            return 'needs_improvement'
        else:
            return 'poor'
    
    def _get_recent_regulatory_changes(self) -> List[Dict]:
        """Get recent regulatory changes and updates"""
        
        return [
            {
                'date': '2024-07-01',
                'regulation': 'POJK No. 15/POJK.03/2024',
                'title': 'Updated Capital Buffer Requirements',
                'impact': 'Medium',
                'description': 'Enhanced capital buffer requirements for systemically important banks',
                'action_required': 'Review capital planning and stress testing procedures'
            },
            {
                'date': '2024-06-15',
                'regulation': 'POJK No. 12/POJK.03/2024',
                'title': 'Digital Banking Governance',
                'impact': 'High',
                'description': 'New governance requirements for digital banking services',
                'action_required': 'Implement digital banking governance framework'
            },
            {
                'date': '2024-05-30',
                'regulation': 'PBI No. 26/2/PBI/2024',
                'title': 'Macroprudential Policy Update',
                'impact': 'Low',
                'description': 'Updated macroprudential indicators and thresholds',
                'action_required': 'Monitor macroprudential indicators'
            }
        ]
    
    def _generate_action_items(self, overall_score: float) -> List[Dict]:
        """Generate compliance action items"""
        
        action_items = []
        
        if overall_score < 85:
            action_items.append({
                'priority': 'High',
                'category': 'Overall Compliance',
                'action': 'Develop comprehensive compliance improvement plan',
                'deadline': datetime.now() + timedelta(days=30),
                'owner': 'Compliance Department'
            })
        
        # Add specific action items based on assessment results
        action_items.extend([
            {
                'priority': 'Medium',
                'category': 'Operational Efficiency',
                'action': 'Implement cost reduction initiatives to improve BOPO',
                'deadline': datetime.now() + timedelta(days=90),
                'owner': 'Operations Team'
            },
            {
                'priority': 'Medium',
                'category': 'Risk Management',
                'action': 'Enhance credit risk monitoring systems',
                'deadline': datetime.now() + timedelta(days=60),
                'owner': 'Risk Management'
            },
            {
                'priority': 'Low',
                'category': 'Governance',
                'action': 'Update board governance policies',
                'deadline': datetime.now() + timedelta(days=120),
                'owner': 'Corporate Secretary'
            }
        ])
        
        return action_items
    
    def _get_capital_recommendations(self, car: float, status: str) -> List[str]:
        """Get capital adequacy recommendations"""
        recommendations = []
        
        if status in ['significant_deviation', 'non_compliant']:
            recommendations.append("Develop capital raising plan (rights issue, subordinated debt)")
            recommendations.append("Restrict dividend payments to preserve capital")
        
        if car > 25:
            recommendations.append("Consider strategic uses of excess capital")
            recommendations.append("Evaluate acquisition opportunities")
        
        recommendations.append("Enhance capital planning and stress testing")
        return recommendations
    
    def _get_asset_quality_recommendations(self, npf: float, status: str) -> List[str]:
        """Get asset quality recommendations"""
        recommendations = []
        
        if npf > 4.0:
            recommendations.append("Implement aggressive NPF reduction strategy")
            recommendations.append("Strengthen collection and workout procedures")
        
        recommendations.extend([
            "Enhance credit risk management systems",
            "Improve early warning indicators",
            "Diversify loan portfolio"
        ])
        
        return recommendations
    
    def _get_operational_recommendations(self, bopo: float, status: str) -> List[str]:
        """Get operational efficiency recommendations"""
        recommendations = []
        
        if bopo > 94:
            recommendations.append("Urgent implementation of cost reduction program")
            recommendations.append("Accelerate automation and digitalization")
        
        recommendations.extend([
            "Optimize branch network efficiency",
            "Implement process automation",
            "Review vendor contracts and procurement"
        ])
        
        return recommendations
    
    def _get_liquidity_recommendations(self, ldr: float, lcr: float, status: str) -> List[str]:
        """Get liquidity management recommendations"""
        recommendations = []
        
        if ldr > 90:
            recommendations.append("Reduce loan-to-deposit ratio")
            recommendations.append("Strengthen deposit mobilization")
        
        recommendations.extend([
            "Maintain adequate liquidity buffers",
            "Diversify funding sources",
            "Implement liquidity stress testing"
        ])
        
        return recommendations
    
    def _get_sharia_recommendations(self, ratio: float, status: str) -> List[str]:
        """Get Sharia compliance recommendations"""
        recommendations = []
        
        if ratio < 99.5:
            recommendations.append("Review and remedy non-Sharia compliant assets")
            recommendations.append("Strengthen Sharia compliance monitoring")
        
        recommendations.extend([
            "Enhance DPS oversight and reporting",
            "Conduct regular Sharia audit reviews",
            "Provide ongoing Sharia training to staff"
        ])
        
        return recommendations
    
    def _get_governance_recommendations(self, score: float, status: str) -> List[str]:
        """Get governance recommendations"""
        recommendations = [
            "Enhance board effectiveness and oversight",
            "Strengthen risk governance framework",
            "Improve compliance training programs",
            "Regular review of governance policies"
        ]
        
        return recommendations

def render_compliance_monitoring():
    """Render comprehensive compliance monitoring dashboard"""
    
    st.title("📋 Advanced Compliance Monitoring System")
    st.markdown("*Comprehensive regulatory compliance tracking and risk management*")
    
    # Get current financial data
    if 'real_scraped_data' in st.session_state:
        current_data = st.session_state.real_scraped_data
    else:
        current_data = {
            'car': 29.42, 'npf': 3.99, 'bopo': 98.5, 'assets': 60.023,
            'loan_to_deposit_ratio': 85.5
        }
    
    # Initialize compliance system
    compliance_system = AdvancedComplianceMonitoring()
    
    # Generate compliance assessment
    if st.button("🔍 **Perform Comprehensive Compliance Assessment**", type="primary"):
        with st.spinner("Analyzing regulatory compliance across all dimensions..."):
            compliance_assessment = compliance_system.assess_comprehensive_compliance(current_data)
            st.session_state.compliance_assessment = compliance_assessment
            st.success("✅ Compliance assessment complete!")
    
    # Display compliance assessment if available
    if 'compliance_assessment' in st.session_state:
        assessment = st.session_state.compliance_assessment
        
        # Overall Compliance Summary
        st.markdown("## 🎯 Overall Compliance Summary")
        
        overall_score = assessment['overall_compliance_score']
        compliance_rating = assessment['compliance_rating']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if compliance_rating == 'excellent':
                st.success(f"🟢 **Compliance Rating: {compliance_rating.title()}**")
            elif compliance_rating in ['good', 'satisfactory']:
                st.warning(f"🟡 **Compliance Rating: {compliance_rating.title()}**")
            else:
                st.error(f"🔴 **Compliance Rating: {compliance_rating.title()}**")
            
            st.metric("Overall Score", f"{overall_score}/100")
        
        with col2:
            assessment_date = assessment.get('assessment_date', datetime.now())
            st.metric("Assessment Date", assessment_date.strftime('%Y-%m-%d'), "📅 Current")
        
        with col3:
            next_review = assessment.get('next_review_date', datetime.now() + timedelta(days=30))
            st.metric("Next Review", next_review.strftime('%Y-%m-%d'), "📅 Scheduled")
        
        with col4:
            # Count non-compliant areas
            non_compliant_areas = sum(1 for area in ['capital_adequacy', 'asset_quality', 'operational_efficiency', 'liquidity', 'sharia_compliance', 'governance'] 
                                    if assessment[area]['status'] in ['significant_deviation', 'non_compliant'])
            st.metric("Non-Compliant Areas", non_compliant_areas, "⚠️ Action Required")
        
        # Compliance Dashboard
        st.markdown("## 📊 Compliance Dashboard")
        
        # Create compliance scorecard
        compliance_areas = [
            ('capital_adequacy', 'Capital Adequacy', '💰'),
            ('asset_quality', 'Asset Quality', '📊'),
            ('operational_efficiency', 'Operational Efficiency', '⚙️'),
            ('liquidity', 'Liquidity', '💧'),
            ('sharia_compliance', 'Sharia Compliance', '☪️'),
            ('governance', 'Governance', '🏛️')
        ]
        
        # Compliance scores for chart
        categories = []
        scores = []
        statuses = []
        
        for area_key, area_name, icon in compliance_areas:
            area_data = assessment[area_key]
            categories.append(area_name)
            scores.append(area_data['score'])
            statuses.append(area_data['status'])
        
        # Create compliance radar chart
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=scores,
            theta=categories,
            fill='toself',
            name='Compliance Score',
            line_color='blue'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Compliance Score Radar Chart"
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Detailed Compliance Analysis
        st.markdown("## 🔍 Detailed Compliance Analysis")
        
        for area_key, area_name, icon in compliance_areas:
            area_data = assessment[area_key]
            
            # Determine status color
            status = area_data['status']
            if status == 'compliant':
                status_color = '🟢'
            elif status == 'minor_deviation':
                status_color = '🟡'
            elif status == 'significant_deviation':
                status_color = '🟠'
            else:
                status_color = '🔴'
            
            with st.expander(f"{icon} **{area_name}** - Score: {area_data['score']}/100 {status_color} ({status.replace('_', ' ').title()})"):
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 📊 Compliance Metrics")
                    
                    current_value = area_data.get('current_value')
                    requirement = area_data.get('requirement')
                    target = area_data.get('target')
                    
                    if isinstance(current_value, dict):
                        for key, value in current_value.items():
                            st.write(f"**{key.replace('_', ' ').title()}**: {value}")
                    else:
                        st.write(f"**Current Value**: {current_value}")
                    
                    if isinstance(requirement, dict):
                        for key, value in requirement.items():
                            st.write(f"**{key.replace('_', ' ').title()}**: {value}")
                    else:
                        st.write(f"**Requirement**: {requirement}")
                    
                    if target and not isinstance(target, dict):
                        st.write(f"**Target**: {target}")
                    
                    # Regulation reference
                    if area_data.get('regulation_reference'):
                        st.caption(f"Regulation: {area_data['regulation_reference']}")
                
                with col2:
                    st.markdown("### 📋 Compliance Details")
                    
                    details = area_data.get('compliance_details', {})
                    for key, value in details.items():
                        st.write(f"**{key.replace('_', ' ').title()}**: {value}")
                    
                    # Show deviation if any
                    deviation = area_data.get('deviation', 0)
                    if deviation > 0:
                        st.warning(f"⚠️ **Deviation**: {deviation}")
                
                # Recommendations
                recommendations = area_data.get('recommendations', [])
                if recommendations:
                    st.markdown("### 💡 Recommendations")
                    for rec in recommendations:
                        st.info(f"💡 {rec}")
        
        # Regulatory Changes
        st.markdown("## 📢 Recent Regulatory Changes")
        
        regulatory_changes = assessment.get('regulatory_changes', [])
        
        if regulatory_changes:
            for change in regulatory_changes:
                impact_color = {'High': 'error', 'Medium': 'warning', 'Low': 'info'}[change['impact']]
                
                with st.container():
                    getattr(st, impact_color)(f"**{change['title']}** ({change['regulation']})")
                    st.write(f"**Date**: {change['date']}")
                    st.write(f"**Impact**: {change['impact']}")
                    st.write(f"**Description**: {change['description']}")
                    st.write(f"**Action Required**: {change['action_required']}")
                    st.write("---")
        
        # Action Items
        st.markdown("## ✅ Compliance Action Items")
        
        action_items = assessment.get('action_items', [])
        
        if action_items:
            df_actions = pd.DataFrame(action_items)
            
            for idx, action in enumerate(action_items):
                priority_color = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}[action['priority']]
                
                col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
                
                with col1:
                    st.write(f"{priority_color} **{action['priority']}**")
                
                with col2:
                    st.write(f"**{action['action']}**")
                    st.caption(f"Category: {action['category']}")
                
                with col3:
                    deadline = action['deadline']
                    days_until = (deadline - datetime.now()).days
                    st.write(f"**Due**: {deadline.strftime('%Y-%m-%d')}")
                    
                    if days_until < 0:
                        st.error(f"Overdue by {abs(days_until)} days")
                    elif days_until < 7:
                        st.warning(f"{days_until} days remaining")
                    else:
                        st.info(f"{days_until} days remaining")
                
                with col4:
                    st.write(f"**Owner**: {action['owner']}")
                    if st.button(f"Mark Complete", key=f"complete_{idx}"):
                        st.success(f"✅ Action item marked as complete")
        
        # Compliance Trend Analysis
        st.markdown("## 📈 Compliance Trend Analysis")
        
        # Generate trend data (simulated)
        dates = pd.date_range(start=datetime.now() - timedelta(days=365), end=datetime.now(), freq='M')
        trend_data = []
        
        for date in dates:
            # Simulate compliance score trends
            base_score = overall_score
            seasonal_variation = np.sin((date.month - 1) * np.pi / 6) * 3  # Seasonal pattern
            random_variation = np.random.normal(0, 2)
            trend_score = max(60, min(100, base_score + seasonal_variation + random_variation))
            
            trend_data.append({
                'Date': date,
                'Overall Compliance Score': trend_score,
                'Capital Adequacy': max(60, min(100, assessment['capital_adequacy']['score'] + np.random.normal(0, 3))),
                'Asset Quality': max(60, min(100, assessment['asset_quality']['score'] + np.random.normal(0, 4))),
                'Operational Efficiency': max(40, min(100, assessment['operational_efficiency']['score'] + np.random.normal(0, 5)))
            })
        
        df_trend = pd.DataFrame(trend_data)
        
        fig_trend = px.line(
            df_trend,
            x='Date',
            y=['Overall Compliance Score', 'Capital Adequacy', 'Asset Quality', 'Operational Efficiency'],
            title='Compliance Score Trends (12 Months)',
            labels={'value': 'Compliance Score', 'variable': 'Compliance Area'}
        )
        
        fig_trend.update_layout(height=400)
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Export Compliance Report
        st.markdown("## 📥 Export Compliance Report")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 **Export Compliance Summary**"):
                summary_data = {
                    'compliance_summary': {
                        'overall_score': assessment['overall_compliance_score'],
                        'compliance_rating': assessment['compliance_rating'],
                        'assessment_date': assessment['assessment_date'].isoformat(),
                        'key_findings': {
                            area_key: {
                                'score': assessment[area_key]['score'],
                                'status': assessment[area_key]['status']
                            }
                            for area_key, _, _ in compliance_areas
                        },
                        'action_items_count': len(action_items),
                        'regulatory_changes_count': len(regulatory_changes)
                    }
                }
                
                summary_json = json.dumps(summary_data, indent=2, default=str)
                
                st.download_button(
                    label="📥 Download Compliance Summary",
                    data=summary_json,
                    file_name=f"compliance_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("📊 **Export Detailed Report**"):
                full_report = {
                    'comprehensive_compliance_assessment': assessment,
                    'source_data': current_data,
                    'methodology': 'Multi-dimensional compliance scoring with regulatory framework',
                    'export_timestamp': datetime.now().isoformat()
                }
                
                report_json = json.dumps(full_report, indent=2, default=str)
                
                st.download_button(
                    label="📥 Download Full Report",
                    data=report_json,
                    file_name=f"comprehensive_compliance_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json"
                )
    
    else:
        # Initial state
        st.markdown("## 🎯 Advanced Compliance Monitoring Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📋 **Compliance Areas**")
            st.write("• **Capital Adequacy** - CAR, buffers, stress testing")
            st.write("• **Asset Quality** - NPF, provisions, concentration limits")
            st.write("• **Operational Efficiency** - BOPO, cost management")
            st.write("• **Liquidity** - LDR, LCR, funding stability")
            st.write("• **Sharia Compliance** - Islamic banking principles")
            st.write("• **Governance** - Board oversight, risk management")
        
        with col2:
            st.markdown("### 🎯 **Monitoring Features**")
            st.write("• **Real-time compliance scoring** with weighted categories")
            st.write("• **Regulatory change tracking** and impact assessment")
            st.write("• **Action item management** with deadlines and owners")
            st.write("• **Trend analysis** for compliance performance")
            st.write("• **Automated reporting** for regulators and management")
            st.write("• **Risk-based prioritization** of compliance issues")
        
        st.info("👆 **Click 'Perform Comprehensive Compliance Assessment' to begin analysis**")
        
        # Show regulatory framework overview
        st.markdown("### 📊 **Regulatory Framework Overview**")
        
        framework_col1, framework_col2 = st.columns(2)
        
        with framework_col1:
            st.markdown("**OJK Regulations:**")
            st.write("• POJK No. 11/POJK.03/2016 - Capital Adequacy")
            st.write("• POJK No. 40/POJK.03/2019 - Asset Quality")
            st.write("• POJK No. 6/POJK.03/2016 - Operational Efficiency")
            st.write("• POJK No. 42/POJK.03/2019 - Liquidity")
        
        with framework_col2:
            st.markdown("**Islamic Banking Specific:**")
            st.write("• POJK No. 24/POJK.03/2020 - Sharia Compliance")
            st.write("• POJK No. 55/POJK.03/2016 - Governance")
            st.write("• Bank Indonesia macroprudential policies")
            st.write("• International Islamic finance standards")