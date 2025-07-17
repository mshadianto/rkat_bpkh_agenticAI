"""
Bank Metrics Models for Bank Muamalat
Defines metrics, ratios, and indicators for bank health monitoring
"""

from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import pandas as pd
import numpy as np

class MetricStatus(Enum):
    """Metric status levels"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"

class RiskLevel(Enum):
    """Risk level categories"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class BankMetrics:
    """
    Core bank metrics data model
    """
    # Identification
    bank_code: str = "MUAMALAT"
    period: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Financial metrics (in billions IDR except ratios)
    total_assets: float = 0.0
    total_liabilities: float = 0.0
    total_equity: float = 0.0
    total_financing: float = 0.0
    total_deposits: float = 0.0
    
    # Profitability metrics
    net_profit: float = 0.0
    operating_income: float = 0.0
    operating_expense: float = 0.0
    net_margin: float = 0.0
    
    # Key ratios (in percentage)
    car: float = 0.0  # Capital Adequacy Ratio
    npf_gross: float = 0.0  # Non-Performing Financing Gross
    npf_net: float = 0.0  # Non-Performing Financing Net
    roa: float = 0.0  # Return on Assets
    roe: float = 0.0  # Return on Equity
    bopo: float = 0.0  # Operating Expense/Operating Income
    fdr: float = 0.0  # Financing to Deposit Ratio
    nim: float = 0.0  # Net Interest/Profit Margin
    
    # Liquidity metrics
    lcr: float = 0.0  # Liquidity Coverage Ratio
    nsfr: float = 0.0  # Net Stable Funding Ratio
    cash_ratio: float = 0.0
    
    # Additional metrics
    cost_of_fund: float = 0.0
    yield_on_financing: float = 0.0
    provision_coverage: float = 0.0
    
    def calculate_derived_metrics(self):
        """Calculate derived metrics from base data"""
        # Calculate equity if not provided
        if self.total_equity == 0 and self.total_assets > 0 and self.total_liabilities > 0:
            self.total_equity = self.total_assets - self.total_liabilities
            
        # Calculate ROA if not provided
        if self.roa == 0 and self.total_assets > 0:
            self.roa = (self.net_profit / self.total_assets) * 100
            
        # Calculate ROE if not provided
        if self.roe == 0 and self.total_equity > 0:
            self.roe = (self.net_profit / self.total_equity) * 100
            
        # Calculate BOPO if not provided
        if self.bopo == 0 and self.operating_income > 0:
            self.bopo = (self.operating_expense / self.operating_income) * 100
            
        # Calculate FDR if not provided
        if self.fdr == 0 and self.total_deposits > 0:
            self.fdr = (self.total_financing / self.total_deposits) * 100
            
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'bank_code': self.bank_code,
            'period': self.period,
            'timestamp': self.timestamp.isoformat(),
            'financial_position': {
                'total_assets': self.total_assets,
                'total_liabilities': self.total_liabilities,
                'total_equity': self.total_equity,
                'total_financing': self.total_financing,
                'total_deposits': self.total_deposits
            },
            'profitability': {
                'net_profit': self.net_profit,
                'operating_income': self.operating_income,
                'operating_expense': self.operating_expense,
                'net_margin': self.net_margin
            },
            'key_ratios': {
                'car': self.car,
                'npf_gross': self.npf_gross,
                'npf_net': self.npf_net,
                'roa': self.roa,
                'roe': self.roe,
                'bopo': self.bopo,
                'fdr': self.fdr,
                'nim': self.nim
            },
            'liquidity': {
                'lcr': self.lcr,
                'nsfr': self.nsfr,
                'cash_ratio': self.cash_ratio
            }
        }

@dataclass
class FinancialRatios:
    """
    Financial ratios calculator and analyzer
    """
    metrics: BankMetrics
    
    # Regulatory thresholds
    CAR_MIN: float = 8.0  # OJK minimum
    NPF_MAX: float = 5.0  # OJK maximum
    FDR_MAX: float = 100.0  # OJK maximum
    BOPO_EFFICIENT: float = 85.0  # Industry benchmark
    ROA_HEALTHY: float = 1.5  # Industry benchmark
    ROE_HEALTHY: float = 15.0  # Industry benchmark
    
    def analyze_capital_adequacy(self) -> Dict[str, Any]:
        """Analyze capital adequacy"""
        car = self.metrics.car
        
        # Determine status
        if car >= self.CAR_MIN * 1.5:  # 50% buffer
            status = MetricStatus.HEALTHY
        elif car >= self.CAR_MIN:
            status = MetricStatus.WARNING
        else:
            status = MetricStatus.CRITICAL
            
        return {
            'value': car,
            'status': status.value,
            'minimum': self.CAR_MIN,
            'buffer': car - self.CAR_MIN,
            'interpretation': self._interpret_car(car)
        }
        
    def analyze_asset_quality(self) -> Dict[str, Any]:
        """Analyze asset quality (NPF)"""
        npf = self.metrics.npf_gross
        
        # Determine status
        if npf <= 2.0:
            status = MetricStatus.HEALTHY
        elif npf <= self.NPF_MAX:
            status = MetricStatus.WARNING
        else:
            status = MetricStatus.CRITICAL
            
        return {
            'npf_gross': npf,
            'npf_net': self.metrics.npf_net,
            'status': status.value,
            'maximum': self.NPF_MAX,
            'margin': self.NPF_MAX - npf,
            'provision_coverage': self.metrics.provision_coverage,
            'interpretation': self._interpret_npf(npf)
        }
        
    def analyze_profitability(self) -> Dict[str, Any]:
        """Analyze profitability metrics"""
        roa = self.metrics.roa
        roe = self.metrics.roe
        nim = self.metrics.nim
        
        # ROA status
        if roa >= self.ROA_HEALTHY:
            roa_status = MetricStatus.HEALTHY
        elif roa >= 0.5:
            roa_status = MetricStatus.WARNING
        else:
            roa_status = MetricStatus.CRITICAL
            
        # ROE status
        if roe >= self.ROE_HEALTHY:
            roe_status = MetricStatus.HEALTHY
        elif roe >= 5.0:
            roe_status = MetricStatus.WARNING
        else:
            roe_status = MetricStatus.CRITICAL
            
        return {
            'roa': {
                'value': roa,
                'status': roa_status.value,
                'benchmark': self.ROA_HEALTHY
            },
            'roe': {
                'value': roe,
                'status': roe_status.value,
                'benchmark': self.ROE_HEALTHY
            },
            'nim': {
                'value': nim,
                'trend': 'stable'  # Calculate from historical data
            },
            'overall_status': self._determine_overall_status([roa_status, roe_status])
        }
        
    def analyze_efficiency(self) -> Dict[str, Any]:
        """Analyze operational efficiency"""
        bopo = self.metrics.bopo
        
        # Determine status
        if bopo <= 80.0:
            status = MetricStatus.HEALTHY
        elif bopo <= self.BOPO_EFFICIENT:
            status = MetricStatus.WARNING
        else:
            status = MetricStatus.CRITICAL
            
        return {
            'bopo': bopo,
            'status': status.value,
            'benchmark': self.BOPO_EFFICIENT,
            'efficiency_gap': bopo - self.BOPO_EFFICIENT,
            'cost_income_ratio': bopo,
            'interpretation': self._interpret_bopo(bopo)
        }
        
    def analyze_liquidity(self) -> Dict[str, Any]:
        """Analyze liquidity position"""
        fdr = self.metrics.fdr
        lcr = self.metrics.lcr
        nsfr = self.metrics.nsfr
        
        # FDR status
        if fdr <= 85.0:
            fdr_status = MetricStatus.HEALTHY
        elif fdr <= self.FDR_MAX:
            fdr_status = MetricStatus.WARNING
        else:
            fdr_status = MetricStatus.CRITICAL
            
        return {
            'fdr': {
                'value': fdr,
                'status': fdr_status.value,
                'maximum': self.FDR_MAX
            },
            'lcr': {
                'value': lcr,
                'minimum': 100.0,
                'compliant': lcr >= 100.0
            },
            'nsfr': {
                'value': nsfr,
                'minimum': 100.0,
                'compliant': nsfr >= 100.0
            },
            'overall_liquidity': self._assess_liquidity_health(fdr, lcr, nsfr)
        }
        
    def calculate_composite_score(self) -> float:
        """Calculate composite health score (0-100)"""
        weights = {
            'capital': 0.25,
            'asset_quality': 0.30,
            'profitability': 0.20,
            'efficiency': 0.15,
            'liquidity': 0.10
        }
        
        scores = {
            'capital': self._score_car(self.metrics.car),
            'asset_quality': self._score_npf(self.metrics.npf_gross),
            'profitability': self._score_profitability(self.metrics.roa, self.metrics.roe),
            'efficiency': self._score_bopo(self.metrics.bopo),
            'liquidity': self._score_liquidity(self.metrics.fdr)
        }
        
        composite = sum(scores[k] * weights[k] for k in weights)
        return round(composite, 2)
        
    def _interpret_car(self, car: float) -> str:
        """Interpret CAR value"""
        if car >= 20:
            return "Very strong capital position"
        elif car >= 15:
            return "Strong capital position"
        elif car >= self.CAR_MIN:
            return "Adequate capital position"
        else:
            return "Capital position below regulatory minimum"
            
    def _interpret_npf(self, npf: float) -> str:
        """Interpret NPF value"""
        if npf <= 2:
            return "Excellent asset quality"
        elif npf <= 3:
            return "Good asset quality"
        elif npf <= self.NPF_MAX:
            return "Asset quality needs attention"
        else:
            return "Poor asset quality - exceeds regulatory limit"
            
    def _interpret_bopo(self, bopo: float) -> str:
        """Interpret BOPO value"""
        if bopo <= 70:
            return "Highly efficient operations"
        elif bopo <= 85:
            return "Efficient operations"
        elif bopo <= 95:
            return "Inefficient operations"
        else:
            return "Very inefficient operations"
            
    def _determine_overall_status(self, statuses: List[MetricStatus]) -> str:
        """Determine overall status from multiple metrics"""
        if all(s == MetricStatus.HEALTHY for s in statuses):
            return MetricStatus.HEALTHY.value
        elif any(s == MetricStatus.CRITICAL for s in statuses):
            return MetricStatus.CRITICAL.value
        else:
            return MetricStatus.WARNING.value
            
    def _assess_liquidity_health(self, fdr: float, lcr: float, nsfr: float) -> str:
        """Assess overall liquidity health"""
        if fdr <= 85 and lcr >= 120 and nsfr >= 110:
            return "Strong liquidity position"
        elif fdr <= 95 and lcr >= 100 and nsfr >= 100:
            return "Adequate liquidity position"
        else:
            return "Liquidity needs monitoring"
            
    def _score_car(self, car: float) -> float:
        """Score CAR (0-100)"""
        if car >= self.CAR_MIN * 2:  # Double the minimum
            return 100
        elif car >= self.CAR_MIN:
            return 50 + (car - self.CAR_MIN) / self.CAR_MIN * 50
        else:
            return max(0, car / self.CAR_MIN * 50)
            
    def _score_npf(self, npf: float) -> float:
        """Score NPF (0-100, inverse)"""
        if npf <= 1:
            return 100
        elif npf <= self.NPF_MAX:
            return 100 - (npf / self.NPF_MAX * 50)
        else:
            return max(0, 50 - (npf - self.NPF_MAX) * 10)
            
    def _score_profitability(self, roa: float, roe: float) -> float:
        """Score profitability (0-100)"""
        roa_score = min(100, (roa / self.ROA_HEALTHY) * 100)
        roe_score = min(100, (roe / self.ROE_HEALTHY) * 100)
        return (roa_score + roe_score) / 2
        
    def _score_bopo(self, bopo: float) -> float:
        """Score BOPO (0-100, inverse)"""
        if bopo <= 70:
            return 100
        elif bopo <= self.BOPO_EFFICIENT:
            return 85 - (bopo - 70) * 1.5
        else:
            return max(0, 50 - (bopo - self.BOPO_EFFICIENT) * 2)
            
    def _score_liquidity(self, fdr: float) -> float:
        """Score liquidity (0-100)"""
        if fdr <= 80:
            return 100
        elif fdr <= self.FDR_MAX:
            return 100 - (fdr - 80) * 2.5
        else:
            return max(0, 50 - (fdr - self.FDR_MAX) * 5)

@dataclass
class RiskIndicators:
    """
    Risk indicators and early warning signals
    """
    metrics: BankMetrics
    historical_data: Optional[pd.DataFrame] = None
    
    def calculate_risk_indicators(self) -> Dict[str, Any]:
        """Calculate comprehensive risk indicators"""
        return {
            'credit_risk': self._calculate_credit_risk(),
            'operational_risk': self._calculate_operational_risk(),
            'market_risk': self._calculate_market_risk(),
            'liquidity_risk': self._calculate_liquidity_risk(),
            'capital_risk': self._calculate_capital_risk(),
            'concentration_risk': self._calculate_concentration_risk()
        }
        
    def generate_early_warnings(self) -> List[Dict[str, Any]]:
        """Generate early warning signals"""
        warnings = []
        
        # NPF warning
        if self.metrics.npf_gross > 3.5:
            warnings.append({
                'type': 'credit_risk',
                'severity': 'high' if self.metrics.npf_gross > 4.5 else 'medium',
                'indicator': 'NPF approaching regulatory limit',
                'value': self.metrics.npf_gross,
                'threshold': 5.0,
                'action': 'Initiate NPF reduction program'
            })
            
        # CAR warning
        if self.metrics.car < 10:
            warnings.append({
                'type': 'capital_risk',
                'severity': 'high' if self.metrics.car < 9 else 'medium',
                'indicator': 'CAR approaching minimum',
                'value': self.metrics.car,
                'threshold': 8.0,
                'action': 'Prepare capital strengthening plan'
            })
            
        # BOPO warning
        if self.metrics.bopo > 90:
            warnings.append({
                'type': 'operational_risk',
                'severity': 'high' if self.metrics.bopo > 95 else 'medium',
                'indicator': 'Operating efficiency deteriorating',
                'value': self.metrics.bopo,
                'threshold': 95.0,
                'action': 'Accelerate cost optimization'
            })
            
        # Profitability warning
        if self.metrics.roa < 0.5:
            warnings.append({
                'type': 'profitability_risk',
                'severity': 'high' if self.metrics.roa < 0 else 'medium',
                'indicator': 'Low profitability',
                'value': self.metrics.roa,
                'threshold': 0.5,
                'action': 'Review revenue enhancement strategies'
            })
            
        return warnings
        
    def _calculate_credit_risk(self) -> Dict[str, Any]:
        """Calculate credit risk indicators"""
        npf = self.metrics.npf_gross
        
        # Determine risk level
        if npf <= 2:
            risk_level = RiskLevel.LOW
        elif npf <= 3.5:
            risk_level = RiskLevel.MEDIUM
        elif npf <= 5:
            risk_level = RiskLevel.HIGH
        else:
            risk_level = RiskLevel.CRITICAL
            
        return {
            'level': risk_level.value,
            'score': self._score_credit_risk(npf),
            'npf_gross': npf,
            'npf_net': self.metrics.npf_net,
            'provision_coverage': self.metrics.provision_coverage,
            'trend': self._calculate_trend('npf_gross') if self.historical_data is not None else 'unknown'
        }
        
    def _calculate_operational_risk(self) -> Dict[str, Any]:
        """Calculate operational risk indicators"""
        bopo = self.metrics.bopo
        
        # Determine risk level
        if bopo <= 80:
            risk_level = RiskLevel.LOW
        elif bopo <= 90:
            risk_level = RiskLevel.MEDIUM
        elif bopo <= 95:
            risk_level = RiskLevel.HIGH
        else:
            risk_level = RiskLevel.CRITICAL
            
        return {
            'level': risk_level.value,
            'score': self._score_operational_risk(bopo),
            'bopo': bopo,
            'cost_income_ratio': bopo,
            'trend': self._calculate_trend('bopo') if self.historical_data is not None else 'unknown'
        }
        
    def _calculate_market_risk(self) -> Dict[str, Any]:
        """Calculate market risk indicators"""
        # Simplified market risk assessment
        return {
            'level': RiskLevel.MEDIUM.value,
            'score': 50,
            'rate_risk': 'moderate',
            'fx_risk': 'low',
            'equity_risk': 'minimal'
        }
        
    def _calculate_liquidity_risk(self) -> Dict[str, Any]:
        """Calculate liquidity risk indicators"""
        fdr = self.metrics.fdr
        
        # Determine risk level
        if fdr <= 80:
            risk_level = RiskLevel.LOW
        elif fdr <= 90:
            risk_level = RiskLevel.MEDIUM
        elif fdr <= 100:
            risk_level = RiskLevel.HIGH
        else:
            risk_level = RiskLevel.CRITICAL
            
        return {
            'level': risk_level.value,
            'score': self._score_liquidity_risk(fdr),
            'fdr': fdr,
            'lcr': self.metrics.lcr,
            'nsfr': self.metrics.nsfr,
            'cash_ratio': self.metrics.cash_ratio
        }
        
    def _calculate_capital_risk(self) -> Dict[str, Any]:
        """Calculate capital risk indicators"""
        car = self.metrics.car
        
        # Determine risk level
        if car >= 15:
            risk_level = RiskLevel.LOW
        elif car >= 12:
            risk_level = RiskLevel.MEDIUM
        elif car >= 8:
            risk_level = RiskLevel.HIGH
        else:
            risk_level = RiskLevel.CRITICAL
            
        return {
            'level': risk_level.value,
            'score': self._score_capital_risk(car),
            'car': car,
            'tier1_ratio': car * 0.8,  # Approximation
            'leverage_ratio': self.metrics.total_assets / self.metrics.total_equity if self.metrics.total_equity > 0 else 0
        }
        
    def _calculate_concentration_risk(self) -> Dict[str, Any]:
        """Calculate concentration risk indicators"""
        # Simplified concentration risk
        return {
            'level': RiskLevel.MEDIUM.value,
            'score': 60,
            'sector_concentration': 'moderate',
            'geographic_concentration': 'high',
            'product_concentration': 'moderate',
            'depositor_concentration': 'low'
        }
        
    def _score_credit_risk(self, npf: float) -> float:
        """Score credit risk (0-100)"""
        if npf <= 1:
            return 10
        elif npf <= 2:
            return 20 + (npf - 1) * 20
        elif npf <= 3.5:
            return 40 + (npf - 2) / 1.5 * 20
        elif npf <= 5:
            return 60 + (npf - 3.5) / 1.5 * 20
        else:
            return min(100, 80 + (npf - 5) * 10)
            
    def _score_operational_risk(self, bopo: float) -> float:
        """Score operational risk (0-100)"""
        if bopo <= 70:
            return 10
        elif bopo <= 80:
            return 10 + (bopo - 70) * 2
        elif bopo <= 90:
            return 30 + (bopo - 80) * 3
        elif bopo <= 95:
            return 60 + (bopo - 90) * 6
        else:
            return min(100, 90 + (bopo - 95) * 2)
            
    def _score_liquidity_risk(self, fdr: float) -> float:
        """Score liquidity risk (0-100)"""
        if fdr <= 70:
            return 10
        elif fdr <= 80:
            return 10 + (fdr - 70) * 2
        elif fdr <= 90:
            return 30 + (fdr - 80) * 3
        elif fdr <= 100:
            return 60 + (fdr - 90) * 3
        else:
            return min(100, 90 + (fdr - 100))
            
    def _score_capital_risk(self, car: float) -> float:
        """Score capital risk (0-100, inverse)"""
        if car >= 20:
            return 10
        elif car >= 15:
            return 10 + (20 - car) * 4
        elif car >= 12:
            return 30 + (15 - car) * 10
        elif car >= 8:
            return 60 + (12 - car) * 7.5
        else:
            return min(100, 90 + (8 - car) * 5)
            
    def _calculate_trend(self, metric: str) -> str:
        """Calculate trend for a metric"""
        if self.historical_data is None or len(self.historical_data) < 3:
            return 'unknown'
            
        # Simple trend calculation
        recent_values = self.historical_data[metric].tail(3)
        if recent_values.is_monotonic_increasing:
            return 'improving' if metric in ['car', 'roa', 'roe'] else 'deteriorating'
        elif recent_values.is_monotonic_decreasing:
            return 'deteriorating' if metric in ['car', 'roa', 'roe'] else 'improving'
        else:
            return 'stable'

@dataclass
class PerformanceMetrics:
    """
    Performance metrics tracker and analyzer
    """
    current_metrics: BankMetrics
    previous_metrics: Optional[BankMetrics] = None
    target_metrics: Optional[Dict[str, float]] = None
    
    def calculate_performance(self) -> Dict[str, Any]:
        """Calculate performance against targets and previous period"""
        performance = {
            'vs_target': self._calculate_vs_target() if self.target_metrics else None,
            'vs_previous': self._calculate_vs_previous() if self.previous_metrics else None,
            'key_achievements': self._identify_achievements(),
            'areas_of_concern': self._identify_concerns(),
            'overall_rating': self._calculate_overall_rating()
        }
        
        return performance
        
    def _calculate_vs_target(self) -> Dict[str, Any]:
        """Calculate performance vs targets"""
        if not self.target_metrics:
            return {}
            
        results = {}
        metrics_map = {
            'car': self.current_metrics.car,
            'npf': self.current_metrics.npf_gross,
            'roa': self.current_metrics.roa,
            'roe': self.current_metrics.roe,
            'bopo': self.current_metrics.bopo,
            'fdr': self.current_metrics.fdr
        }
        
        for metric, current_value in metrics_map.items():
            if metric in self.target_metrics:
                target = self.target_metrics[metric]
                variance = current_value - target
                variance_pct = (variance / target * 100) if target != 0 else 0
                
                # Determine if meeting target (considering metric direction)
                if metric in ['npf', 'bopo']:  # Lower is better
                    meeting_target = current_value <= target
                else:  # Higher is better
                    meeting_target = current_value >= target
                    
                results[metric] = {
                    'current': current_value,
                    'target': target,
                    'variance': variance,
                    'variance_pct': variance_pct,
                    'meeting_target': meeting_target
                }
                
        return results
        
    def _calculate_vs_previous(self) -> Dict[str, Any]:
        """Calculate performance vs previous period"""
        if not self.previous_metrics:
            return {}
            
        results = {}
        metrics_pairs = [
            ('car', self.current_metrics.car, self.previous_metrics.car),
            ('npf', self.current_metrics.npf_gross, self.previous_metrics.npf_gross),
            ('roa', self.current_metrics.roa, self.previous_metrics.roa),
            ('roe', self.current_metrics.roe, self.previous_metrics.roe),
            ('bopo', self.current_metrics.bopo, self.previous_metrics.bopo),
            ('fdr', self.current_metrics.fdr, self.previous_metrics.fdr)
        ]
        
        for metric, current, previous in metrics_pairs:
            change = current - previous
            change_pct = (change / previous * 100) if previous != 0 else 0
            
            # Determine if improving (considering metric direction)
            if metric in ['npf', 'bopo']:  # Lower is better
                improving = change < 0
            else:  # Higher is better
                improving = change > 0
                
            results[metric] = {
                'current': current,
                'previous': previous,
                'change': change,
                'change_pct': change_pct,
                'trend': 'improving' if improving else 'deteriorating' if change != 0 else 'stable'
            }
            
        return results
        
    def _identify_achievements(self) -> List[str]:
        """Identify key achievements"""
        achievements = []
        
        # Strong capital position
        if self.current_metrics.car >= 20:
            achievements.append(f"Strong capital position with CAR at {self.current_metrics.car}%")
            
        # Low NPF
        if self.current_metrics.npf_gross <= 2:
            achievements.append(f"Excellent asset quality with NPF at {self.current_metrics.npf_gross}%")
            
        # Good profitability
        if self.current_metrics.roa >= 1.5:
            achievements.append(f"Strong profitability with ROA at {self.current_metrics.roa}%")
            
        # Efficiency
        if self.current_metrics.bopo <= 80:
            achievements.append(f"Efficient operations with BOPO at {self.current_metrics.bopo}%")
            
        return achievements
        
    def _identify_concerns(self) -> List[str]:
        """Identify areas of concern"""
        concerns = []
        
        # High NPF
        if self.current_metrics.npf_gross > 3:
            concerns.append(f"Asset quality concern with NPF at {self.current_metrics.npf_gross}%")
            
        # Low profitability
        if self.current_metrics.roa < 0.5:
            concerns.append(f"Low profitability with ROA at {self.current_metrics.roa}%")
            
        # Poor efficiency
        if self.current_metrics.bopo > 90:
            concerns.append(f"Operational inefficiency with BOPO at {self.current_metrics.bopo}%")
            
        # Capital pressure
        if self.current_metrics.car < 12:
            concerns.append(f"Capital buffer narrowing with CAR at {self.current_metrics.car}%")
            
        return concerns
        
    def _calculate_overall_rating(self) -> str:
        """Calculate overall performance rating"""
        # Simple rating based on key metrics
        score = 0
        
        # CAR contribution
        if self.current_metrics.car >= 15:
            score += 25
        elif self.current_metrics.car >= 12:
            score += 15
        elif self.current_metrics.car >= 8:
            score += 5
            
        # NPF contribution
        if self.current_metrics.npf_gross <= 2:
            score += 25
        elif self.current_metrics.npf_gross <= 3.5:
            score += 15
        elif self.current_metrics.npf_gross <= 5:
            score += 5
            
        # ROA contribution
        if self.current_metrics.roa >= 1.5:
            score += 25
        elif self.current_metrics.roa >= 0.5:
            score += 15
        elif self.current_metrics.roa >= 0:
            score += 5
            
        # BOPO contribution
        if self.current_metrics.bopo <= 80:
            score += 25
        elif self.current_metrics.bopo <= 90:
            score += 15
        elif self.current_metrics.bopo <= 95:
            score += 5
            
        # Determine rating
        if score >= 80:
            return "EXCELLENT"
        elif score >= 60:
            return "GOOD"
        elif score >= 40:
            return "SATISFACTORY"
        elif score >= 20:
            return "NEEDS IMPROVEMENT"
        else:
            return "POOR"

@dataclass
class ComplianceMetrics:
    """
    Compliance metrics and regulatory indicators
    """
    metrics: BankMetrics
    
    def check_regulatory_compliance(self) -> Dict[str, Any]:
        """Check compliance with all regulatory requirements"""
        return {
            'ojk_compliance': self._check_ojk_compliance(),
            'basel_compliance': self._check_basel_compliance(),
            'sharia_compliance': self._check_sharia_compliance(),
            'overall_compliance_status': self._determine_overall_compliance()
        }
        
    def _check_ojk_compliance(self) -> Dict[str, Any]:
        """Check OJK regulatory compliance"""
        compliance_items = {
            'car': {
                'requirement': 8.0,
                'current': self.metrics.car,
                'compliant': self.metrics.car >= 8.0,
                'regulation': 'POJK No.11/POJK.03/2016'
            },
            'npf': {
                'requirement': 5.0,
                'current': self.metrics.npf_gross,
                'compliant': self.metrics.npf_gross <= 5.0,
                'regulation': 'POJK No.15/POJK.03/2017'
            },
            'fdr': {
                'requirement': 100.0,
                'current': self.metrics.fdr,
                'compliant': self.metrics.fdr <= 100.0,
                'regulation': 'POJK No.04/POJK.03/2016'
            },
            'lcr': {
                'requirement': 100.0,
                'current': self.metrics.lcr,
                'compliant': self.metrics.lcr >= 100.0,
                'regulation': 'POJK No.42/POJK.03/2015'
            },
            'nsfr': {
                'requirement': 100.0,
                'current': self.metrics.nsfr,
                'compliant': self.metrics.nsfr >= 100.0,
                'regulation': 'POJK No.50/POJK.03/2017'
            }
        }
        
        # Count compliant items
        compliant_count = sum(1 for item in compliance_items.values() if item['compliant'])
        total_count = len(compliance_items)
        
        return {
            'items': compliance_items,
            'compliant_count': compliant_count,
            'total_count': total_count,
            'compliance_rate': (compliant_count / total_count * 100),
            'status': 'FULLY COMPLIANT' if compliant_count == total_count else 'PARTIALLY COMPLIANT'
        }
        
    def _check_basel_compliance(self) -> Dict[str, Any]:
        """Check Basel III compliance"""
        return {
            'capital_requirement': {
                'minimum_car': 8.0,
                'capital_conservation_buffer': 2.5,
                'total_requirement': 10.5,
                'current': self.metrics.car,
                'compliant': self.metrics.car >= 10.5
            },
            'leverage_ratio': {
                'requirement': 3.0,
                'current': self._calculate_leverage_ratio(),
                'compliant': self._calculate_leverage_ratio() >= 3.0
            },
            'liquidity_requirements': {
                'lcr_compliant': self.metrics.lcr >= 100.0,
                'nsfr_compliant': self.metrics.nsfr >= 100.0
            }
        }
        
    def _check_sharia_compliance(self) -> Dict[str, Any]:
        """Check Sharia compliance indicators"""
        return {
            'sharia_supervisory_board': 'Active',
            'fatwa_compliance': 'Compliant',
            'income_purification': 'Implemented',
            'zakat_calculation': 'Proper',
            'product_compliance': 'All products Sharia-compliant',
            'sharia_audit_findings': 'No major violations'
        }
        
    def _determine_overall_compliance(self) -> str:
        """Determine overall compliance status"""
        ojk_status = self._check_ojk_compliance()['status']
        basel_compliant = self._check_basel_compliance()['capital_requirement']['compliant']
        
        if ojk_status == 'FULLY COMPLIANT' and basel_compliant:
            return 'FULLY COMPLIANT'
        elif ojk_status == 'PARTIALLY COMPLIANT' or not basel_compliant:
            return 'PARTIALLY COMPLIANT'
        else:
            return 'NON-COMPLIANT'
            
    def _calculate_leverage_ratio(self) -> float:
        """Calculate leverage ratio"""
        if self.metrics.total_equity > 0:
            return (self.metrics.total_equity / self.metrics.total_assets) * 100
        return 0.0