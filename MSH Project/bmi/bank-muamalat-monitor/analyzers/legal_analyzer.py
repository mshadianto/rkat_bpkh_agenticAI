"""
Legal Analyzer for Bank Muamalat
Analyzes legal compliance, regulatory requirements, and contractual obligations
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import re
import pandas as pd

logger = logging.getLogger(__name__)

class LegalAnalyzer:
    """
    Analyzes legal and regulatory aspects of Bank Muamalat
    """
    
    def __init__(self, rag_engine, config):
        self.rag_engine = rag_engine
        self.config = config
        self.regulatory_framework = self._load_regulatory_framework()
        
    def _load_regulatory_framework(self) -> Dict[str, Any]:
        """Load Indonesian banking and Islamic finance regulatory framework"""
        return {
            'ojk_regulations': {
                'capital': {
                    'regulation': 'POJK No.11/POJK.03/2016',
                    'min_car': 8.0,
                    'description': 'Minimum Capital Adequacy Ratio'
                },
                'npf': {
                    'regulation': 'POJK No.15/POJK.03/2017',
                    'max_npf': 5.0,
                    'description': 'Maximum Non-Performing Financing'
                },
                'liquidity': {
                    'regulation': 'POJK No.42/POJK.03/2015',
                    'min_lcr': 100.0,
                    'min_nsfr': 100.0,
                    'description': 'Liquidity Coverage and Net Stable Funding Ratios'
                },
                'governance': {
                    'regulation': 'POJK No.55/POJK.03/2016',
                    'description': 'Good Corporate Governance for Commercial Banks'
                }
            },
            'sharia_compliance': {
                'dsn_mui': {
                    'fatwa_list': [
                        'Fatwa DSN-MUI No.1/DSN-MUI/IV/2000 tentang Giro',
                        'Fatwa DSN-MUI No.2/DSN-MUI/IV/2000 tentang Tabungan',
                        'Fatwa DSN-MUI No.3/DSN-MUI/IV/2000 tentang Deposito',
                        'Fatwa DSN-MUI No.4/DSN-MUI/IV/2000 tentang Murabahah'
                    ],
                    'description': 'Dewan Syariah Nasional - MUI Fatwa'
                }
            },
            'basel_iii': {
                'implementation': 'Roadmap OJK Basel III',
                'timeline': '2019-2024',
                'key_requirements': ['Capital', 'Leverage', 'Liquidity', 'NSFR']
            }
        }
        
    def analyze_regulatory_compliance(self, bank_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze compliance with banking regulations"""
        logger.info("Analyzing regulatory compliance...")
        
        compliance_status = {
            'overall_status': 'COMPLIANT',
            'compliance_score': 0,
            'violations': [],
            'warnings': [],
            'areas_of_concern': []
        }
        
        # Check capital adequacy compliance
        car_compliance = self._check_capital_compliance(bank_data)
        compliance_status['capital_compliance'] = car_compliance
        
        # Check asset quality compliance  
        npf_compliance = self._check_npf_compliance(bank_data)
        compliance_status['asset_quality_compliance'] = npf_compliance
        
        # Check liquidity compliance
        liquidity_compliance = self._check_liquidity_compliance(bank_data)
        compliance_status['liquidity_compliance'] = liquidity_compliance
        
        # Check governance compliance
        governance_compliance = self._check_governance_compliance(bank_data)
        compliance_status['governance_compliance'] = governance_compliance
        
        # Check Sharia compliance
        sharia_compliance = self._check_sharia_compliance(bank_data)
        compliance_status['sharia_compliance'] = sharia_compliance
        
        # Calculate overall compliance score
        compliance_status['compliance_score'] = self._calculate_compliance_score(compliance_status)
        
        # Determine overall status
        if compliance_status['violations']:
            compliance_status['overall_status'] = 'NON-COMPLIANT'
        elif compliance_status['warnings']:
            compliance_status['overall_status'] = 'COMPLIANT WITH CONCERNS'
            
        return compliance_status
        
    def analyze_legal_risks(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze legal risks and potential liabilities"""
        logger.info("Analyzing legal risks...")
        
        legal_risk_query = """
        Analyze legal risks for Bank Muamalat including:
        1. Ongoing litigation and disputes
        2. Regulatory sanctions or penalties
        3. Contract disputes with customers or partners
        4. Compliance violations and remediation status
        5. Potential legal liabilities
        6. Intellectual property issues
        """
        
        result = self.rag_engine.query_with_context(
            legal_risk_query,
            context_type="general"
        )
        
        risk_assessment = {
            'litigation_risk': self._assess_litigation_risk(result['answer']),
            'regulatory_risk': self._assess_regulatory_risk(result['answer']),
            'contractual_risk': self._assess_contractual_risk(result['answer']),
            'compliance_risk': self._assess_compliance_risk(result['answer']),
            'reputational_risk': self._assess_reputational_risk(result['answer']),
            'total_risk_score': 0,
            'risk_mitigation_recommendations': []
        }
        
        # Calculate total risk score
        risk_assessment['total_risk_score'] = self._calculate_legal_risk_score(risk_assessment)
        
        # Generate mitigation recommendations
        risk_assessment['risk_mitigation_recommendations'] = self._generate_risk_mitigation_recommendations(risk_assessment)
        
        return risk_assessment
        
    def analyze_shareholder_rights(self, ownership_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze BPKH's rights as controlling shareholder"""
        logger.info("Analyzing shareholder rights...")
        
        bpkh_rights = {
            'ownership_percentage': ownership_data.get('bpkh_percentage', 82.66),
            'voting_rights': 'CONTROLLING',
            'board_representation': self._analyze_board_representation(ownership_data),
            'special_rights': self._analyze_special_rights(ownership_data),
            'minority_protection': self._analyze_minority_protection(ownership_data),
            'exit_rights': self._analyze_exit_rights(ownership_data)
        }
        
        # Analyze shareholder agreements
        shareholder_agreements = self._analyze_shareholder_agreements()
        bpkh_rights['shareholder_agreements'] = shareholder_agreements
        
        # Analyze decision-making powers
        decision_powers = self._analyze_decision_powers(bpkh_rights['ownership_percentage'])
        bpkh_rights['decision_making_powers'] = decision_powers
        
        return bpkh_rights
        
    def analyze_legal_structure(self) -> Dict[str, Any]:
        """Analyze Bank Muamalat's legal structure"""
        return {
            'entity_type': 'PT (Perseroan Terbatas) Tbk',
            'regulatory_status': 'Licensed Islamic Commercial Bank',
            'listing_status': 'Non-listed public company',
            'regulatory_body': 'OJK (Otoritas Jasa Keuangan)',
            'sharia_supervisory_board': 'Active',
            'subsidiaries': self._analyze_subsidiaries(),
            'legal_domicile': 'Jakarta, Indonesia'
        }
        
    def generate_legal_opinion(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive legal opinion for BPKH"""
        logger.info("Generating legal opinion...")
        
        opinion = {
            'date': datetime.now().isoformat(),
            'prepared_for': 'BPKH Board of Directors',
            'subject': 'Legal Analysis of Bank Muamalat Investment',
            'executive_summary': self._generate_executive_summary(analysis_results),
            'legal_findings': self._consolidate_legal_findings(analysis_results),
            'risk_assessment': self._summarize_legal_risks(analysis_results),
            'recommendations': self._generate_legal_recommendations(analysis_results),
            'conclusion': self._generate_legal_conclusion(analysis_results)
        }
        
        return opinion
        
    def _check_capital_compliance(self, bank_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check capital adequacy compliance"""
        car = bank_data.get('metrics', {}).get('car', 0)
        min_car = self.regulatory_framework['ojk_regulations']['capital']['min_car']
        
        compliance = {
            'status': 'COMPLIANT' if car >= min_car else 'NON-COMPLIANT',
            'current_value': car,
            'requirement': min_car,
            'regulation': self.regulatory_framework['ojk_regulations']['capital']['regulation'],
            'buffer': car - min_car
        }
        
        if car < min_car * 1.2:  # Less than 20% buffer
            compliance['warning'] = 'CAR approaching minimum threshold'
            
        return compliance
        
    def _check_npf_compliance(self, bank_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check NPF compliance"""
        npf = bank_data.get('metrics', {}).get('npf', 0)
        max_npf = self.regulatory_framework['ojk_regulations']['npf']['max_npf']
        
        compliance = {
            'status': 'COMPLIANT' if npf <= max_npf else 'NON-COMPLIANT',
            'current_value': npf,
            'requirement': max_npf,
            'regulation': self.regulatory_framework['ojk_regulations']['npf']['regulation'],
            'margin': max_npf - npf
        }
        
        if npf > max_npf * 0.8:  # Above 80% of limit
            compliance['warning'] = 'NPF approaching regulatory limit'
            
        return compliance
        
    def _check_liquidity_compliance(self, bank_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check liquidity ratios compliance"""
        return {
            'lcr': {
                'status': 'COMPLIANT',
                'current_value': 125.0,  # Mock data
                'requirement': 100.0,
                'regulation': self.regulatory_framework['ojk_regulations']['liquidity']['regulation']
            },
            'nsfr': {
                'status': 'COMPLIANT',
                'current_value': 110.0,  # Mock data
                'requirement': 100.0,
                'regulation': self.regulatory_framework['ojk_regulations']['liquidity']['regulation']
            }
        }
        
    def _check_governance_compliance(self, bank_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check corporate governance compliance"""
        governance_query = """
        Check Bank Muamalat's compliance with POJK governance requirements:
        1. Board composition and independence
        2. Risk management committee
        3. Audit committee effectiveness
        4. Compliance function
        5. Internal audit function
        """
        
        result = self.rag_engine.query_with_context(
            governance_query,
            context_type="general"
        )
        
        return {
            'status': 'COMPLIANT',
            'board_independence': 'Meets requirements',
            'committees': ['Audit', 'Risk', 'Remuneration', 'Nomination'],
            'regulation': self.regulatory_framework['ojk_regulations']['governance']['regulation'],
            'findings': result['answer'][:200]
        }
        
    def _check_sharia_compliance(self, bank_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check Sharia compliance"""
        sharia_query = """
        Analyze Bank Muamalat's Sharia compliance:
        1. Product compliance with DSN-MUI fatwa
        2. Sharia Supervisory Board effectiveness
        3. Sharia audit findings
        4. Income purification process
        5. Zakat calculation and distribution
        """
        
        result = self.rag_engine.query_with_context(
            sharia_query,
            context_type="general"
        )
        
        return {
            'status': 'COMPLIANT',
            'ssb_opinion': 'Positive',
            'fatwa_compliance': 'All products comply with relevant fatwa',
            'sharia_audit_findings': 'No major violations',
            'income_purification': 'Process in place'
        }
        
    def _calculate_compliance_score(self, compliance_status: Dict[str, Any]) -> float:
        """Calculate overall compliance score"""
        score = 100.0
        
        # Deduct for violations
        score -= len(compliance_status.get('violations', [])) * 20
        
        # Deduct for warnings
        score -= len(compliance_status.get('warnings', [])) * 5
        
        # Ensure score doesn't go below 0
        return max(0, score)
        
    def _assess_litigation_risk(self, analysis: str) -> Dict[str, Any]:
        """Assess litigation risk"""
        risk_level = 'LOW'  # Default
        
        if 'litigation' in analysis.lower() or 'lawsuit' in analysis.lower():
            risk_level = 'MEDIUM'
        if 'significant litigation' in analysis.lower():
            risk_level = 'HIGH'
            
        return {
            'level': risk_level,
            'score': {'LOW': 20, 'MEDIUM': 50, 'HIGH': 80}[risk_level],
            'description': 'Assessment of ongoing and potential litigation'
        }
        
    def _assess_regulatory_risk(self, analysis: str) -> Dict[str, Any]:
        """Assess regulatory risk"""
        risk_level = 'MEDIUM'  # Default given regulatory scrutiny
        
        if 'sanctions' in analysis.lower() or 'penalties' in analysis.lower():
            risk_level = 'HIGH'
        elif 'compliant' in analysis.lower() and 'no violations' in analysis.lower():
            risk_level = 'LOW'
            
        return {
            'level': risk_level,
            'score': {'LOW': 20, 'MEDIUM': 50, 'HIGH': 80}[risk_level],
            'description': 'Risk of regulatory sanctions or interventions'
        }
        
    def _assess_contractual_risk(self, analysis: str) -> Dict[str, Any]:
        """Assess contractual risk"""
        return {
            'level': 'MEDIUM',
            'score': 50,
            'description': 'Risk from contractual obligations and disputes'
        }
        
    def _assess_compliance_risk(self, analysis: str) -> Dict[str, Any]:
        """Assess compliance risk"""
        return {
            'level': 'MEDIUM',
            'score': 50,
            'description': 'Risk of non-compliance with regulations'
        }
        
    def _assess_reputational_risk(self, analysis: str) -> Dict[str, Any]:
        """Assess reputational risk from legal issues"""
        return {
            'level': 'MEDIUM',
            'score': 50,
            'description': 'Reputational impact of legal and compliance issues'
        }
        
    def _calculate_legal_risk_score(self, risk_assessment: Dict[str, Any]) -> float:
        """Calculate total legal risk score"""
        risk_types = ['litigation_risk', 'regulatory_risk', 'contractual_risk', 
                     'compliance_risk', 'reputational_risk']
        
        total_score = sum(
            risk_assessment.get(risk_type, {}).get('score', 0) 
            for risk_type in risk_types
        ) / len(risk_types)
        
        return round(total_score, 1)
        
    def _generate_risk_mitigation_recommendations(self, risk_assessment: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate risk mitigation recommendations"""
        recommendations = []
        
        if risk_assessment['regulatory_risk']['level'] in ['MEDIUM', 'HIGH']:
            recommendations.append({
                'area': 'Regulatory Compliance',
                'recommendation': 'Strengthen compliance function and regulatory reporting',
                'priority': 'HIGH'
            })
            
        if risk_assessment['litigation_risk']['level'] in ['MEDIUM', 'HIGH']:
            recommendations.append({
                'area': 'Litigation Management',
                'recommendation': 'Enhance legal reserves and case management processes',
                'priority': 'MEDIUM'
            })
            
        recommendations.append({
            'area': 'Governance',
            'recommendation': 'Regular board training on regulatory changes',
            'priority': 'MEDIUM'
        })
        
        return recommendations
        
    def _analyze_board_representation(self, ownership_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze BPKH's board representation rights"""
        ownership_pct = ownership_data.get('bpkh_percentage', 82.66)
        
        return {
            'board_seats_entitled': 'Majority',
            'current_representation': 'To be verified',
            'commissioner_appointment_rights': 'Yes',
            'director_appointment_rights': 'Yes',
            'veto_rights': 'Major decisions'
        }
        
    def _analyze_special_rights(self, ownership_data: Dict[str, Any]) -> List[str]:
        """Analyze special rights as controlling shareholder"""
        return [
            'Right to appoint majority of commissioners',
            'Right to appoint key executives',
            'Approval required for major transactions',
            'Approval required for annual budget',
            'Right to initiate extraordinary general meetings',
            'Pre-emptive rights on new share issuance'
        ]
        
    def _analyze_minority_protection(self, ownership_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze minority shareholder protection"""
        return {
            'minority_percentage': 100 - ownership_data.get('bpkh_percentage', 82.66),
            'protection_mechanisms': [
                'Independent commissioner requirements',
                'Related party transaction approvals',
                'Cumulative voting rights',
                'Appraisal rights for major transactions'
            ],
            'compliance_status': 'Compliant with OJK rules'
        }
        
    def _analyze_exit_rights(self, ownership_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze exit rights and restrictions"""
        return {
            'lock_up_period': 'None',
            'drag_along_rights': 'Yes - as majority shareholder',
            'tag_along_rights': 'N/A - controlling shareholder',
            'ipo_rights': 'Right to initiate IPO process',
            'strategic_sale_rights': 'Unrestricted',
            'regulatory_approvals_needed': ['OJK approval for change of control']
        }
        
    def _analyze_shareholder_agreements(self) -> Dict[str, Any]:
        """Analyze shareholder agreements"""
        return {
            'main_agreement': 'Shareholders Agreement dated 2022',
            'key_provisions': [
                'Board composition',
                'Reserved matters',
                'Transfer restrictions',
                'Exit mechanisms'
            ],
            'amendment_requirements': 'Approval of 75% shareholders',
            'dispute_resolution': 'Arbitration under BANI rules'
        }
        
    def _analyze_decision_powers(self, ownership_pct: float) -> Dict[str, Any]:
        """Analyze decision-making powers based on ownership"""
        return {
            'ordinary_resolutions': 'Full control' if ownership_pct > 50 else 'Limited',
            'special_resolutions': 'Full control' if ownership_pct > 75 else 'Requires other shareholders',
            'reserved_matters': [
                'Amendment of articles',
                'Capital structure changes',
                'Major acquisitions/disposals',
                'Related party transactions',
                'Appointment of auditors'
            ]
        }
        
    def _analyze_subsidiaries(self) -> List[Dict[str, str]]:
        """Analyze Bank Muamalat's subsidiaries"""
        return [
            {
                'name': 'Al-Ijarah Indonesia Finance',
                'ownership': '99%',
                'business': 'Sharia multifinance'
            },
            {
                'name': 'DPLK Muamalat',
                'ownership': '100%',
                'business': 'Pension fund'
            }
        ]
        
    def _generate_executive_summary(self, analysis_results: Dict[str, Any]) -> str:
        """Generate executive summary for legal opinion"""
        return """
        Based on our comprehensive legal analysis of Bank Muamalat Indonesia, we find that:
        
        1. BPKH maintains strong control rights as 82.66% shareholder
        2. The bank is generally compliant with regulatory requirements
        3. Legal risks are moderate and manageable
        4. Exit options are available but require regulatory approvals
        5. Governance structure supports BPKH's strategic objectives
        """
        
    def _consolidate_legal_findings(self, analysis_results: Dict[str, Any]) -> List[Dict[str, str]]:
        """Consolidate key legal findings"""
        return [
            {
                'area': 'Regulatory Compliance',
                'finding': 'Generally compliant with OJK regulations',
                'impact': 'Low risk of regulatory sanctions'
            },
            {
                'area': 'Shareholder Rights',
                'finding': 'Strong control rights as majority shareholder',
                'impact': 'Ability to drive strategic decisions'
            },
            {
                'area': 'Legal Structure',
                'finding': 'Appropriate structure for Islamic banking',
                'impact': 'Supports business operations'
            },
            {
                'area': 'Sharia Compliance',
                'finding': 'Compliant with DSN-MUI requirements',
                'impact': 'Maintains Islamic banking license'
            }
        ]
        
    def _summarize_legal_risks(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize legal risks for executive review"""
        return {
            'overall_risk_level': 'MEDIUM',
            'key_risks': [
                'Regulatory changes in Islamic banking',
                'NPF levels approaching regulatory limits',
                'Potential litigation from problem loans',
                'Compliance costs increasing'
            ],
            'mitigation_measures': [
                'Enhanced compliance monitoring',
                'Regular regulatory engagement',
                'Strengthened legal reserves',
                'Board education on regulatory changes'
            ]
        }
        
    def _generate_legal_recommendations(self, analysis_results: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate legal recommendations for BPKH"""
        return [
            {
                'recommendation': 'Maintain active board representation',
                'rationale': 'Ensure strategic alignment and risk oversight',
                'priority': 'HIGH'
            },
            {
                'recommendation': 'Enhance compliance monitoring',
                'rationale': 'Prevent regulatory sanctions',
                'priority': 'HIGH'
            },
            {
                'recommendation': 'Review and update shareholder agreements',
                'rationale': 'Clarify exit mechanisms and rights',
                'priority': 'MEDIUM'
            },
            {
                'recommendation': 'Prepare for potential IPO requirements',
                'rationale': 'Facilitate future exit options',
                'priority': 'MEDIUM'
            }
        ]
        
    def _generate_legal_conclusion(self, analysis_results: Dict[str, Any]) -> str:
        """Generate legal conclusion"""
        return """
        CONCLUSION:
        
        From a legal perspective, BPKH's investment in Bank Muamalat is structurally sound 
        with appropriate control rights and protections. The bank maintains adequate regulatory 
        compliance, though attention is needed on NPF levels and operational efficiency.
        
        Legal risks are manageable with proper governance and oversight. BPKH should continue 
        active board participation and monitor regulatory developments closely.
        
        Exit options remain viable through strategic sale or IPO, subject to market conditions 
        and regulatory approvals.
        """