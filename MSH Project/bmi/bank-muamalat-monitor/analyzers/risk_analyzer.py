"""
Risk Analyzer Module
Comprehensive risk analysis and early warning system for Bank Muamalat
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
from enum import Enum
import json

logger = logging.getLogger(__name__)

class RiskLevel(Enum):
    """Risk level enumeration"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

@dataclass
class RiskMetrics:
    """Risk metrics data structure"""
    credit_risk_score: float
    market_risk_score: float
    operational_risk_score: float
    liquidity_risk_score: float
    compliance_risk_score: float
    strategic_risk_score: float
    reputational_risk_score: float
    shariah_risk_score: float
    timestamp: datetime

class RiskAnalyzer:
    """
    Advanced risk analysis system for Bank Muamalat
    """
    
    def __init__(self, config):
        self.config = config
        self.risk_weights = self._initialize_risk_weights()
        self.risk_thresholds = self._initialize_risk_thresholds()
        self.early_warning_indicators = self._initialize_early_warnings()
        
    def _initialize_risk_weights(self) -> Dict[str, float]:
        """Initialize risk category weights"""
        return {
            'credit': 0.30,
            'market': 0.10,
            'operational': 0.20,
            'liquidity': 0.15,
            'compliance': 0.10,
            'strategic': 0.10,
            'reputational': 0.05
        }
        
    def _initialize_risk_thresholds(self) -> Dict[str, Dict[str, float]]:
        """Initialize risk thresholds"""
        return {
            'credit': {
                'low': 25,
                'medium': 50,
                'high': 75,
                'critical': 90
            },
            'operational': {
                'low': 30,
                'medium': 55,
                'high': 80,
                'critical': 95
            },
            'liquidity': {
                'low': 20,
                'medium': 45,
                'high': 70,
                'critical': 85
            },
            'compliance': {
                'low': 20,
                'medium': 40,
                'high': 65,
                'critical': 85
            }
        }
        
    def _initialize_early_warnings(self) -> Dict[str, Any]:
        """Initialize early warning indicators"""
        return {
            'credit': {
                'npf_threshold': 3.5,
                'npf_growth_rate': 0.5,  # per quarter
                'concentration_limit': 25,  # % of portfolio
                'coverage_ratio_min': 100
            },
            'liquidity': {
                'fdr_warning': 95,
                'fdr_critical': 100,
                'lcr_minimum': 100,
                'deposit_volatility_max': 10  # %
            },
            'operational': {
                'bopo_warning': 90,
                'bopo_critical': 95,
                'system_downtime_max': 0.1,  # %
                'fraud_incidents_max': 5  # per quarter
            },
            'compliance': {
                'regulatory_breaches_max': 0,
                'audit_findings_max': 5,
                'training_completion_min': 95  # %
            }
        }
        
    def analyze_comprehensive_risk(
        self, 
        financial_data: Dict[str, Any],
        operational_data: Optional[Dict[str, Any]] = None,
        market_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Perform comprehensive risk analysis
        """
        logger.info("Starting comprehensive risk analysis")
        
        # Analyze individual risk categories
        credit_risk = self._analyze_credit_risk(financial_data)
        market_risk = self._analyze_market_risk(financial_data, market_data)
        operational_risk = self._analyze_operational_risk(financial_data, operational_data)
        liquidity_risk = self._analyze_liquidity_risk(financial_data)
        compliance_risk = self._analyze_compliance_risk(financial_data, operational_data)
        strategic_risk = self._analyze_strategic_risk(financial_data)
        reputational_risk = self._analyze_reputational_risk(financial_data, operational_data)
        shariah_risk = self._analyze_shariah_risk(financial_data)
        
        # Calculate composite risk score
        composite_score = self._calculate_composite_risk_score({
            'credit': credit_risk['score'],
            'market': market_risk['score'],
            'operational': operational_risk['score'],
            'liquidity': liquidity_risk['score'],
            'compliance': compliance_risk['score'],
            'strategic': strategic_risk['score'],
            'reputational': reputational_risk['score']
        })
        
        # Generate risk matrix
        risk_matrix = self._generate_risk_matrix({
            'credit': credit_risk,
            'market': market_risk,
            'operational': operational_risk,
            'liquidity': liquidity_risk,
            'compliance': compliance_risk,
            'strategic': strategic_risk,
            'reputational': reputational_risk,
            'shariah': shariah_risk
        })
        
        # Check early warnings
        early_warnings = self._check_early_warnings(financial_data, operational_data)
        
        # Perform stress testing
        stress_test_results = self._perform_comprehensive_stress_test(financial_data)
        
        # Generate risk mitigation strategies
        mitigation_strategies = self._generate_mitigation_strategies(risk_matrix)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'composite_risk_score': composite_score,
            'overall_risk_level': self._determine_overall_risk_level(composite_score),
            'risk_categories': {
                'credit': credit_risk,
                'market': market_risk,
                'operational': operational_risk,
                'liquidity': liquidity_risk,
                'compliance': compliance_risk,
                'strategic': strategic_risk,
                'reputational': reputational_risk,
                'shariah': shariah_risk
            },
            'risk_matrix': risk_matrix,
            'early_warnings': early_warnings,
            'stress_test_results': stress_test_results,
            'mitigation_strategies': mitigation_strategies,
            'risk_appetite_assessment': self._assess_risk_appetite_alignment(composite_score),
            'recommendations': self._generate_risk_recommendations(risk_matrix, early_warnings)
        }
        
    def _analyze_credit_risk(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze credit risk in detail"""
        npf = financial_data.get('npf_gross', 0)
        car = financial_data.get('car', 0)
        coverage_ratio = financial_data.get('coverage_ratio', 0)
        
        # Calculate credit risk score
        score = 0
        
        # NPF component (40% weight)
        if npf <= 2:
            score += 10
        elif npf <= 3:
            score += 20
        elif npf <= 5:
            score += 30
        else:
            score += 40
            
        # Coverage ratio component (30% weight)
        if coverage_ratio >= 150:
            score += 5
        elif coverage_ratio >= 100:
            score += 15
        else:
            score += 30
            
        # Concentration risk (30% weight)
        concentration = self._calculate_concentration_risk(financial_data)
        score += concentration * 0.3
        
        # Risk factors
        risk_factors = []
        if npf > 3:
            risk_factors.append({
                'factor': 'High NPF',
                'impact': 'HIGH',
                'description': f'NPF at {npf}% exceeds acceptable threshold'
            })
            
        if coverage_ratio < 100:
            risk_factors.append({
                'factor': 'Low coverage',
                'impact': 'MEDIUM',
                'description': f'Coverage ratio at {coverage_ratio}% below prudent level'
            })
            
        return {
            'score': score,
            'level': self._get_risk_level(score, 'credit'),
            'components': {
                'npf_score': min(40, npf * 8),
                'coverage_score': max(0, 30 - coverage_ratio * 0.2),
                'concentration_score': concentration * 0.3
            },
            'risk_factors': risk_factors,
            'metrics': {
                'npf_gross': npf,
                'npf_net': financial_data.get('npf_net', 0),
                'coverage_ratio': coverage_ratio,
                'expected_loss': self._calculate_expected_loss(financial_data),
                'unexpected_loss': self._calculate_unexpected_loss(financial_data)
            },
            'trend': self._analyze_credit_trend(financial_data)
        }
        
    def _analyze_market_risk(
        self, 
        financial_data: Dict[str, Any],
        market_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Analyze market risk"""
        score = 30  # Base score for Islamic banks (lower trading exposure)
        
        risk_factors = []
        
        # Profit rate risk
        if financial_data.get('asset_liability_mismatch', 0) > 20:
            score += 20
            risk_factors.append({
                'factor': 'Asset-liability mismatch',
                'impact': 'MEDIUM',
                'description': 'Significant maturity mismatch'
            })
            
        # FX risk (if applicable)
        fx_exposure = financial_data.get('fx_exposure', 0)
        if fx_exposure > 10:
            score += 15
            risk_factors.append({
                'factor': 'FX exposure',
                'impact': 'MEDIUM',
                'description': f'Foreign exchange exposure at {fx_exposure}%'
            })
            
        return {
            'score': score,
            'level': self._get_risk_level(score, 'market'),
            'components': {
                'profit_rate_risk': 20,
                'fx_risk': fx_exposure * 1.5,
                'equity_risk': 5,
                'commodity_risk': 5
            },
            'risk_factors': risk_factors,
            'metrics': {
                'duration_gap': 2.5,  # Mock data
                'fx_exposure': fx_exposure,
                'var_estimate': self._calculate_var(financial_data)
            }
        }
        
    def _analyze_operational_risk(
        self, 
        financial_data: Dict[str, Any],
        operational_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Analyze operational risk"""
        bopo = financial_data.get('bopo', 0)
        
        # Calculate operational risk score
        score = 0
        
        # Efficiency component (40% weight)
        if bopo <= 80:
            score += 10
        elif bopo <= 90:
            score += 25
        else:
            score += 40
            
        # IT risk component (30% weight)
        it_risk = self._assess_it_risk(operational_data)
        score += it_risk * 0.3
        
        # Process risk component (30% weight)
        process_risk = self._assess_process_risk(operational_data)
        score += process_risk * 0.3
        
        risk_factors = []
        if bopo > 90:
            risk_factors.append({
                'factor': 'High operational costs',
                'impact': 'HIGH',
                'description': f'BOPO at {bopo}% indicates inefficiency'
            })
            
        return {
            'score': score,
            'level': self._get_risk_level(score, 'operational'),
            'components': {
                'efficiency_risk': min(40, (bopo - 70) * 1.3),
                'it_risk': it_risk * 0.3,
                'process_risk': process_risk * 0.3,
                'people_risk': 15
            },
            'risk_factors': risk_factors,
            'metrics': {
                'bopo_ratio': bopo,
                'system_availability': 99.5,  # Mock
                'process_automation': 35,  # % Mock
                'fraud_incidents': 2  # Mock
            },
            'operational_losses': self._estimate_operational_losses(operational_data)
        }
        
    def _analyze_liquidity_risk(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze liquidity risk"""
        fdr = financial_data.get('fdr', 0)
        
        # Calculate liquidity risk score
        score = 0
        
        # FDR component (50% weight)
        if fdr <= 85:
            score += 10
        elif fdr <= 95:
            score += 25
        elif fdr <= 100:
            score += 40
        else:
            score += 50
            
        # Funding stability (30% weight)
        funding_stability = self._assess_funding_stability(financial_data)
        score += funding_stability * 0.3
        
        # Liquidity buffer (20% weight)
        buffer_score = max(0, 20 - (100 - fdr) * 0.5) if fdr < 100 else 20
        score += buffer_score
        
        risk_factors = []
        if fdr > 95:
            risk_factors.append({
                'factor': 'High FDR',
                'impact': 'HIGH',
                'description': f'FDR at {fdr}% approaching regulatory limit'
            })
            
        return {
            'score': score,
            'level': self._get_risk_level(score, 'liquidity'),
            'components': {
                'fdr_risk': min(50, (fdr - 70) * 1.67),
                'funding_concentration': 15,
                'maturity_mismatch': 10
            },
            'risk_factors': risk_factors,
            'metrics': {
                'fdr': fdr,
                'lcr_estimate': 120,  # Mock
                'nsfr_estimate': 110,  # Mock
                'liquid_assets_ratio': 15  # Mock
            },
            'stress_scenarios': self._liquidity_stress_scenarios(financial_data)
        }
        
    def _analyze_compliance_risk(
        self, 
        financial_data: Dict[str, Any],
        operational_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Analyze compliance and regulatory risk"""
        score = 30  # Base score
        
        risk_factors = []
        
        # Regulatory compliance
        if financial_data.get('car', 0) < 12:
            score += 30
            risk_factors.append({
                'factor': 'CAR breach',
                'impact': 'CRITICAL',
                'description': 'Below regulatory minimum CAR'
            })
            
        if financial_data.get('npf_gross', 0) > 5:
            score += 20
            risk_factors.append({
                'factor': 'NPF breach',
                'impact': 'HIGH',
                'description': 'Exceeds regulatory NPF limit'
            })
            
        # AML/CFT risk
        aml_score = self._assess_aml_risk(operational_data)
        score += aml_score * 0.2
        
        return {
            'score': score,
            'level': self._get_risk_level(score, 'compliance'),
            'components': {
                'regulatory_compliance': 20,
                'aml_cft_risk': aml_score * 0.2,
                'legal_risk': 10,
                'conduct_risk': 5
            },
            'risk_factors': risk_factors,
            'metrics': {
                'regulatory_breaches': 0,  # Mock
                'pending_litigations': 2,  # Mock
                'audit_findings': 5  # Mock
            },
            'compliance_status': self._assess_compliance_status(financial_data)
        }
        
    def _analyze_strategic_risk(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze strategic and business risk"""
        score = 40  # Base score given current challenges
        
        risk_factors = []
        
        # Market share decline
        score += 15
        risk_factors.append({
            'factor': 'Market share erosion',
            'impact': 'MEDIUM',
            'description': 'Continued loss of market position'
        })
        
        # Digital transformation lag
        score += 20
        risk_factors.append({
            'factor': 'Digital transformation delay',
            'impact': 'HIGH',
            'description': 'Lagging in digital banking adoption'
        })
        
        # Profitability challenges
        if financial_data.get('roa', 0) < 1:
            score += 15
            risk_factors.append({
                'factor': 'Low profitability',
                'impact': 'HIGH',
                'description': 'ROA below sustainable levels'
            })
            
        return {
            'score': score,
            'level': self._get_risk_level(score, 'strategic'),
            'components': {
                'market_position': 35,
                'innovation_gap': 30,
                'execution_risk': 25
            },
            'risk_factors': risk_factors,
            'strategic_initiatives': self._assess_strategic_initiatives()
        }
        
    def _analyze_reputational_risk(
        self, 
        financial_data: Dict[str, Any],
        operational_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Analyze reputational risk"""
        score = 25  # Base score
        
        risk_factors = []
        
        # Financial performance impact
        if financial_data.get('consecutive_losses', 0) > 2:
            score += 20
            risk_factors.append({
                'factor': 'Consecutive losses',
                'impact': 'MEDIUM',
                'description': 'Negative financial headlines'
            })
            
        # Service quality
        if operational_data and operational_data.get('customer_complaints', 0) > 100:
            score += 15
            risk_factors.append({
                'factor': 'Service issues',
                'impact': 'MEDIUM',
                'description': 'Rising customer complaints'
            })
            
        return {
            'score': score,
            'level': self._get_risk_level(score, 'reputational'),
            'risk_factors': risk_factors,
            'metrics': {
                'media_sentiment': 'NEUTRAL',  # Mock
                'customer_satisfaction': 75,  # Mock
                'brand_value_index': 65  # Mock
            }
        }
        
    def _analyze_shariah_risk(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze Shariah compliance risk"""
        score = 15  # Base score for established Islamic bank
        
        risk_factors = []
        
        # Check for Shariah compliance indicators
        non_halal_income = financial_data.get('non_halal_income_ratio', 0)
        if non_halal_income > 5:
            score += 30
            risk_factors.append({
                'factor': 'Non-halal income',
                'impact': 'HIGH',
                'description': f'Non-halal income at {non_halal_income}%'
            })
            
        return {
            'score': score,
            'level': self._get_risk_level(score, 'shariah'),
            'risk_factors': risk_factors,
            'shariah_audit_findings': 2,  # Mock
            'product_compliance': 98  # % Mock
        }
        
    def _calculate_composite_risk_score(self, risk_scores: Dict[str, float]) -> float:
        """Calculate weighted composite risk score"""
        total_score = 0
        
        for risk_type, score in risk_scores.items():
            weight = self.risk_weights.get(risk_type, 0)
            total_score += score * weight
            
        return round(total_score, 2)
        
    def _determine_overall_risk_level(self, composite_score: float) -> str:
        """Determine overall risk level based on composite score"""
        if composite_score < 30:
            return "LOW"
        elif composite_score < 50:
            return "MEDIUM"
        elif composite_score < 70:
            return "HIGH"
        else:
            return "CRITICAL"
            
    def _get_risk_level(self, score: float, risk_type: str) -> str:
        """Get risk level for specific risk type"""
        thresholds = self.risk_thresholds.get(
            risk_type, 
            self.risk_thresholds['credit']
        )
        
        if score < thresholds['low']:
            return "LOW"
        elif score < thresholds['medium']:
            return "MEDIUM"
        elif score < thresholds['high']:
            return "HIGH"
        else:
            return "CRITICAL"
            
    def _check_early_warnings(
        self, 
        financial_data: Dict[str, Any],
        operational_data: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Check for early warning indicators"""
        warnings = []
        
        # Credit risk warnings
        npf = financial_data.get('npf_gross', 0)
        if npf > self.early_warning_indicators['credit']['npf_threshold']:
            warnings.append({
                'category': 'Credit Risk',
                'indicator': 'NPF Threshold',
                'severity': 'HIGH',
                'value': npf,
                'threshold': self.early_warning_indicators['credit']['npf_threshold'],
                'message': f'NPF at {npf}% exceeds warning threshold',
                'action_required': 'Immediate NPF reduction measures'
            })
            
        # Liquidity warnings
        fdr = financial_data.get('fdr', 0)
        if fdr > self.early_warning_indicators['liquidity']['fdr_warning']:
            severity = 'CRITICAL' if fdr > self.early_warning_indicators['liquidity']['fdr_critical'] else 'HIGH'
            warnings.append({
                'category': 'Liquidity Risk',
                'indicator': 'FDR Limit',
                'severity': severity,
                'value': fdr,
                'threshold': self.early_warning_indicators['liquidity']['fdr_warning'],
                'message': f'FDR at {fdr}% in danger zone',
                'action_required': 'Enhance liquidity management'
            })
            
        # Operational warnings
        bopo = financial_data.get('bopo', 0)
        if bopo > self.early_warning_indicators['operational']['bopo_warning']:
            warnings.append({
                'category': 'Operational Risk',
                'indicator': 'BOPO Efficiency',
                'severity': 'HIGH',
                'value': bopo,
                'threshold': self.early_warning_indicators['operational']['bopo_warning'],
                'message': f'BOPO at {bopo}% indicates severe inefficiency',
                'action_required': 'Urgent cost optimization needed'
            })
            
        return warnings
        
    def _generate_risk_matrix(self, risk_categories: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate risk matrix for visualization"""
        matrix = []
        
        for category, data in risk_categories.items():
            impact = self._assess_risk_impact(category, data['score'])
            likelihood = self._assess_risk_likelihood(category, data)
            
            matrix.append({
                'category': category,
                'impact': impact,
                'likelihood': likelihood,
                'score': data['score'],
                'level': data['level'],
                'quadrant': self._determine_quadrant(impact, likelihood)
            })
            
        return sorted(matrix, key=lambda x: x['score'], reverse=True)
        
    def _assess_risk_impact(self, category: str, score: float) -> str:
        """Assess potential impact of risk"""
        if category in ['credit', 'liquidity', 'compliance']:
            if score > 70:
                return "VERY HIGH"
            elif score > 50:
                return "HIGH"
            elif score > 30:
                return "MEDIUM"
            else:
                return "LOW"
        else:
            if score > 60:
                return "HIGH"
            elif score > 40:
                return "MEDIUM"
            else:
                return "LOW"
                
    def _assess_risk_likelihood(self, category: str, risk_data: Dict) -> str:
        """Assess likelihood of risk occurrence"""
        # Simplified logic - in production, use historical data
        score = risk_data['score']
        
        if score > 70:
            return "VERY LIKELY"
        elif score > 50:
            return "LIKELY"
        elif score > 30:
            return "POSSIBLE"
        else:
            return "UNLIKELY"
            
    def _determine_quadrant(self, impact: str, likelihood: str) -> str:
        """Determine risk matrix quadrant"""
        impact_map = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "VERY HIGH": 4}
        likelihood_map = {"UNLIKELY": 1, "POSSIBLE": 2, "LIKELY": 3, "VERY LIKELY": 4}
        
        impact_score = impact_map.get(impact, 2)
        likelihood_score = likelihood_map.get(likelihood, 2)
        
        if impact_score >= 3 and likelihood_score >= 3:
            return "CRITICAL"
        elif impact_score >= 3 or likelihood_score >= 3:
            return "HIGH"
        elif impact_score >= 2 and likelihood_score >= 2:
            return "MEDIUM"
        else:
            return "LOW"
            
    def _perform_comprehensive_stress_test(
        self, 
        financial_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Perform comprehensive stress testing"""
        scenarios = {
            'baseline': {
                'description': 'Current conditions continue',
                'npf_shock': 0,
                'deposit_shock': 0,
                'rate_shock': 0
            },
            'moderate_stress': {
                'description': 'Moderate economic downturn',
                'npf_shock': 3,
                'deposit_shock': -10,
                'rate_shock': 200  # basis points
            },
            'severe_stress': {
                'description': 'Severe recession scenario',
                'npf_shock': 7,
                'deposit_shock': -25,
                'rate_shock': 400
            },
            'pandemic_scenario': {
                'description': 'Pandemic-like disruption',
                'npf_shock': 10,
                'deposit_shock': -30,
                'rate_shock': 300
            }
        }
        
        results = {}
        
        for scenario_name, shocks in scenarios.items():
            stressed_metrics = self._apply_stress_scenario(financial_data, shocks)
            
            results[scenario_name] = {
                'description': shocks['description'],
                'stressed_car': stressed_metrics['car'],
                'stressed_npf': stressed_metrics['npf'],
                'stressed_fdr': stressed_metrics['fdr'],
                'stressed_roa': stressed_metrics['roa'],
                'breaches': self._check_regulatory_breaches(stressed_metrics),
                'survival_probability': self._calculate_survival_probability(stressed_metrics),
                'capital_shortfall': max(0, 12 - stressed_metrics['car']) * stressed_metrics['rwa'] / 100
            }
            
        return results
        
    def _apply_stress_scenario(
        self, 
        financial_data: Dict[str, Any], 
        shocks: Dict[str, float]
    ) -> Dict[str, Any]:
        """Apply stress scenario to financial metrics"""
        # Current metrics
        current_car = financial_data.get('car', 30)
        current_npf = financial_data.get('npf_gross', 4)
        current_deposits = financial_data.get('total_deposits', 100)
        current_rwa = financial_data.get('rwa', 100)
        
        # Apply shocks
        stressed_npf = current_npf + shocks['npf_shock']
        stressed_deposits = current_deposits * (1 + shocks['deposit_shock'] / 100)
        
        # Calculate impact on capital
        additional_provisions = shocks['npf_shock'] * 0.6  # 60% provisioning
        stressed_capital = financial_data.get('total_equity', 30) - additional_provisions
        
        # Calculate stressed CAR
        stressed_car = (stressed_capital / current_rwa) * 100
        
        # Calculate stressed FDR
        stressed_loans = financial_data.get('total_loans', 85)
        stressed_fdr = (stressed_loans / stressed_deposits) * 100
        
        # Calculate stressed ROA
        profit_impact = -shocks['npf_shock'] * 0.3  # 30% profit impact per NPF point
        stressed_roa = max(-2, financial_data.get('roa', 0.5) + profit_impact)
        
        return {
            'car': stressed_car,
            'npf': stressed_npf,
            'fdr': stressed_fdr,
            'roa': stressed_roa,
            'rwa': current_rwa
        }
        
    def _check_regulatory_breaches(self, stressed_metrics: Dict[str, float]) -> List[str]:
        """Check for regulatory breaches under stress"""
        breaches = []
        
        if stressed_metrics['car'] < 8:
            breaches.append(f"CAR breach: {stressed_metrics['car']:.1f}% < 8%")
            
        if stressed_metrics['npf'] > 5:
            breaches.append(f"NPF breach: {stressed_metrics['npf']:.1f}% > 5%")
            
        if stressed_metrics['fdr'] > 110:
            breaches.append(f"FDR breach: {stressed_metrics['fdr']:.1f}% > 110%")
            
        return breaches
        
    def _calculate_survival_probability(self, stressed_metrics: Dict[str, float]) -> float:
        """Calculate probability of surviving stress scenario"""
        survival_score = 100
        
        # CAR impact
        if stressed_metrics['car'] < 8:
            survival_score -= 40
        elif stressed_metrics['car'] < 10:
            survival_score -= 20
        elif stressed_metrics['car'] < 12:
            survival_score -= 10
            
        # NPF impact
        if stressed_metrics['npf'] > 10:
            survival_score -= 30
        elif stressed_metrics['npf'] > 7:
            survival_score -= 20
        elif stressed_metrics['npf'] > 5:
            survival_score -= 10
            
        # Profitability impact
        if stressed_metrics['roa'] < -1:
            survival_score -= 20
        elif stressed_metrics['roa'] < 0:
            survival_score -= 10
            
        return max(0, survival_score)
        
    def _generate_mitigation_strategies(
        self, 
        risk_matrix: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate risk mitigation strategies"""
        strategies = []
        
        # Focus on critical and high risks
        critical_risks = [r for r in risk_matrix if r['quadrant'] in ['CRITICAL', 'HIGH']]
        
        for risk in critical_risks:
            if risk['category'] == 'credit':
                strategies.append({
                    'risk_category': 'Credit Risk',
                    'priority': 'CRITICAL',
                    'strategies': [
                        'Establish specialized NPF workout unit',
                        'Implement stricter credit underwriting',
                        'Accelerate collateral liquidation',
                        'Enhance collection efforts',
                        'Consider portfolio sales for chronic NPF'
                    ],
                    'timeline': '3-6 months',
                    'expected_impact': 'Reduce NPF by 1-2% points',
                    'resource_requirement': 'HIGH'
                })
                
            elif risk['category'] == 'operational':
                strategies.append({
                    'risk_category': 'Operational Risk',
                    'priority': 'HIGH',
                    'strategies': [
                        'Fast-track digital transformation',
                        'Implement robotic process automation',
                        'Optimize branch network',
                        'Outsource non-core functions',
                        'Zero-based budgeting approach'
                    ],
                    'timeline': '12-18 months',
                    'expected_impact': 'Reduce BOPO by 10-15%',
                    'resource_requirement': 'MEDIUM'
                })
                
            elif risk['category'] == 'liquidity':
                strategies.append({
                    'risk_category': 'Liquidity Risk',
                    'priority': 'HIGH',
                    'strategies': [
                        'Diversify funding sources',
                        'Develop Islamic money market instruments',
                        'Enhance deposit mobilization',
                        'Establish credit lines with other banks',
                        'Optimize asset-liability matching'
                    ],
                    'timeline': '6-9 months',
                    'expected_impact': 'Improve liquidity buffers',
                    'resource_requirement': 'MEDIUM'
                })
                
        return sorted(strategies, key=lambda x: {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2}.get(x['priority'], 3))
        
    def _assess_risk_appetite_alignment(self, composite_score: float) -> Dict[str, Any]:
        """Assess alignment with BPKH risk appetite"""
        bpkh_risk_appetite = {
            'target_range': [30, 50],  # Medium risk appetite
            'tolerance_limit': 60,
            'capacity_limit': 70
        }
        
        alignment = {
            'current_risk_score': composite_score,
            'within_appetite': bpkh_risk_appetite['target_range'][0] <= composite_score <= bpkh_risk_appetite['target_range'][1],
            'within_tolerance': composite_score <= bpkh_risk_appetite['tolerance_limit'],
            'within_capacity': composite_score <= bpkh_risk_appetite['capacity_limit']
        }
        
        if not alignment['within_capacity']:
            alignment['status'] = 'CRITICAL - Exceeds risk capacity'
            alignment['action'] = 'Immediate risk reduction required'
        elif not alignment['within_tolerance']:
            alignment['status'] = 'WARNING - Exceeds risk tolerance'
            alignment['action'] = 'Implement risk mitigation measures'
        elif not alignment['within_appetite']:
            alignment['status'] = 'CAUTION - Outside target appetite'
            alignment['action'] = 'Monitor and adjust risk profile'
        else:
            alignment['status'] = 'ACCEPTABLE - Within risk appetite'
            alignment['action'] = 'Maintain current risk management'
            
        return alignment
        
    def _generate_risk_recommendations(
        self, 
        risk_matrix: List[Dict[str, Any]],
        early_warnings: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate comprehensive risk recommendations"""
        recommendations = []
        
        # Priority 1: Address early warnings
        for warning in early_warnings:
            if warning['severity'] in ['CRITICAL', 'HIGH']:
                recommendations.append({
                    'priority': 1,
                    'category': warning['category'],
                    'recommendation': warning['action_required'],
                    'rationale': warning['message'],
                    'timeline': 'Immediate'
                })
                
        # Priority 2: Address critical risks
        critical_risks = [r for r in risk_matrix if r['level'] == 'CRITICAL']
        for risk in critical_risks:
            recommendations.append({
                'priority': 2,
                'category': f"{risk['category'].title()} Risk",
                'recommendation': f"Implement comprehensive {risk['category']} risk mitigation",
                'rationale': f"Risk score at {risk['score']} in critical zone",
                'timeline': '1-3 months'
            })
            
        # Priority 3: Strategic recommendations
        recommendations.append({
            'priority': 3,
            'category': 'Risk Governance',
            'recommendation': 'Enhance risk management framework',
            'rationale': 'Strengthen three lines of defense',
            'timeline': '6 months'
        })
        
        return sorted(recommendations, key=lambda x: x['priority'])
        
    # Helper methods
    def _calculate_concentration_risk(self, financial_data: Dict[str, Any]) -> float:
        """Calculate credit concentration risk"""
        # Simplified calculation
        return 30.0  # Mock value
        
    def _calculate_expected_loss(self, financial_data: Dict[str, Any]) -> float:
        """Calculate expected credit loss"""
        pd = financial_data.get('npf_gross', 0) / 100  # Probability of default
        lgd = 0.45  # Loss given default (45%)
        ead = financial_data.get('total_loans', 100)  # Exposure at default
        
        return pd * lgd * ead
        
    def _calculate_unexpected_loss(self, financial_data: Dict[str, Any]) -> float:
        """Calculate unexpected credit loss"""
        # Simplified calculation
        expected_loss = self._calculate_expected_loss(financial_data)
        return expected_loss * 2.5  # Mock multiplier
        
    def _analyze_credit_trend(self, financial_data: Dict[str, Any]) -> str:
        """Analyze credit risk trend"""
        # Simplified - in production, use historical data
        return "DETERIORATING"
        
    def _calculate_var(self, financial_data: Dict[str, Any]) -> float:
        """Calculate Value at Risk"""
        # Simplified VaR calculation
        return financial_data.get('total_assets', 100) * 0.02  # 2% VaR
        
    def _assess_it_risk(self, operational_data: Optional[Dict[str, Any]]) -> float:
        """Assess IT and cyber risk"""
        if not operational_data:
            return 50  # Default medium risk
            
        score = 0
        
        # System availability
        if operational_data.get('system_availability', 100) < 99.5:
            score += 30
            
        # Cyber incidents
        if operational_data.get('cyber_incidents', 0) > 0:
            score += 40
            
        # System age
        if operational_data.get('core_system_age', 0) > 10:
            score += 30
            
        return min(100, score)
        
    def _assess_process_risk(self, operational_data: Optional[Dict[str, Any]]) -> float:
        """Assess business process risk"""
        if not operational_data:
            return 60  # Default higher risk due to manual processes
            
        automation_rate = operational_data.get('process_automation', 30)
        return max(0, 100 - automation_rate * 1.5)
        
    def _assess_funding_stability(self, financial_data: Dict[str, Any]) -> float:
        """Assess funding stability score"""
        # Simplified calculation
        casa_ratio = financial_data.get('casa_ratio', 50)
        deposit_concentration = financial_data.get('deposit_concentration', 25)
        
        stability_score = (casa_ratio * 0.6) + ((100 - deposit_concentration) * 0.4)
        return min(100, stability_score)
        
    def _liquidity_stress_scenarios(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate liquidity stress scenarios"""
        return {
            'deposit_run': {
                'outflow_1_day': 5,  # %
                'outflow_1_week': 15,
                'outflow_1_month': 25,
                'survival_days': 45  # Mock
            },
            'market_freeze': {
                'funding_gap': 10,  # billion IDR
                'contingent_funding': 15,
                'survival_probability': 85  # %
            }
        }
        
    def _assess_aml_risk(self, operational_data: Optional[Dict[str, Any]]) -> float:
        """Assess AML/CFT risk"""
        if not operational_data:
            return 40  # Default medium risk
            
        score = 0
        
        # STR filings
        if operational_data.get('str_filings', 0) > 50:
            score += 30
            
        # High-risk customers
        if operational_data.get('high_risk_customers_pct', 0) > 10:
            score += 40
            
        # Training completion
        if operational_data.get('aml_training_completion', 100) < 95:
            score += 30
            
        return min(100, score)
        
    def _assess_compliance_status(self, financial_data: Dict[str, Any]) -> Dict[str, str]:
        """Assess regulatory compliance status"""
        status = {}
        
        # CAR compliance
        car = financial_data.get('car', 0)
        if car >= 12:
            status['car'] = 'COMPLIANT'
        elif car >= 10:
            status['car'] = 'WARNING'
        else:
            status['car'] = 'BREACH'
            
        # NPF compliance
        npf = financial_data.get('npf_gross', 0)
        if npf <= 5:
            status['npf'] = 'COMPLIANT'
        else:
            status['npf'] = 'BREACH'
            
        # FDR compliance
        fdr = financial_data.get('fdr', 0)
        if fdr <= 100:
            status['fdr'] = 'COMPLIANT'
        elif fdr <= 110:
            status['fdr'] = 'WARNING'
        else:
            status['fdr'] = 'BREACH'
            
        return status
        
    def _assess_strategic_initiatives(self) -> List[Dict[str, str]]:
        """Assess strategic initiatives and their risk impact"""
        return [
            {
                'initiative': 'Digital Transformation',
                'status': 'IN_PROGRESS',
                'risk_impact': 'Reduces operational risk',
                'completion': '35%'
            },
            {
                'initiative': 'NPF Recovery Program',
                'status': 'PLANNING',
                'risk_impact': 'Reduces credit risk',
                'completion': '10%'
            },
            {
                'initiative': 'BPKH Ecosystem Integration',
                'status': 'ACTIVE',
                'risk_impact': 'Reduces strategic risk',
                'completion': '60%'
            }
        ]