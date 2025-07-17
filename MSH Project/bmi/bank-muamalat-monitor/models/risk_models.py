"""
Risk Models for Bank Muamalat
Statistical and ML models for risk assessment and scoring
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import logging
from dataclasses import dataclass
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

@dataclass
class RiskMetrics:
    """Data class for risk metrics"""
    npf_ratio: float
    car_ratio: float
    fdr_ratio: float
    bopo_ratio: float
    roa: float
    roe: float
    liquidity_ratio: float
    concentration_risk: float
    market_share: float
    gdp_growth: float
    inflation_rate: float
    bi_rate: float

class CreditRiskModel:
    """
    Credit risk model for NPF prediction and analysis
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_importance = {}
        self.risk_thresholds = {
            'low': 2.0,
            'medium': 3.5,
            'high': 5.0,
            'critical': 7.0
        }
        
    def calculate_expected_loss(
        self,
        exposure: float,
        pd: float,
        lgd: float
    ) -> float:
        """
        Calculate Expected Loss (EL)
        EL = EAD × PD × LGD
        """
        return exposure * pd * lgd
        
    def calculate_pd(self, risk_metrics: RiskMetrics) -> float:
        """
        Calculate Probability of Default based on risk metrics
        """
        # Simplified PD model based on key indicators
        base_pd = 0.02  # 2% base probability
        
        # Adjust based on NPF level
        if risk_metrics.npf_ratio > 5:
            pd_adjustment = 0.05
        elif risk_metrics.npf_ratio > 3:
            pd_adjustment = 0.03
        elif risk_metrics.npf_ratio > 2:
            pd_adjustment = 0.01
        else:
            pd_adjustment = 0
            
        # Adjust based on economic indicators
        macro_adjustment = (
            (risk_metrics.inflation_rate - 3.0) * 0.005 +
            (6.0 - risk_metrics.gdp_growth) * 0.003 +
            (risk_metrics.bi_rate - 5.0) * 0.002
        )
        
        # Adjust based on operational efficiency
        if risk_metrics.bopo_ratio > 95:
            efficiency_adjustment = 0.02
        elif risk_metrics.bopo_ratio > 85:
            efficiency_adjustment = 0.01
        else:
            efficiency_adjustment = 0
            
        pd = base_pd + pd_adjustment + macro_adjustment + efficiency_adjustment
        
        # Ensure PD is between 0 and 1
        return max(0.001, min(0.999, pd))
        
    def calculate_lgd(self, collateral_coverage: float, recovery_rate: float) -> float:
        """
        Calculate Loss Given Default
        LGD = 1 - Recovery Rate
        """
        base_recovery = 0.4  # 40% base recovery
        
        # Adjust for collateral
        collateral_adjustment = min(0.3, collateral_coverage * 0.5)
        
        # Adjust for historical recovery
        recovery_adjustment = recovery_rate * 0.2
        
        total_recovery = base_recovery + collateral_adjustment + recovery_adjustment
        
        # LGD is 1 minus recovery rate
        lgd = 1 - min(0.95, total_recovery)
        
        return max(0.05, lgd)
        
    def stress_test_credit_risk(
        self,
        current_metrics: RiskMetrics,
        scenarios: Dict[str, Dict[str, float]]
    ) -> Dict[str, Any]:
        """
        Perform credit risk stress testing
        """
        results = {}
        
        for scenario_name, adjustments in scenarios.items():
            # Apply stress adjustments
            stressed_metrics = RiskMetrics(
                npf_ratio=current_metrics.npf_ratio * (1 + adjustments.get('npf_shock', 0)),
                car_ratio=current_metrics.car_ratio * (1 + adjustments.get('car_shock', 0)),
                fdr_ratio=current_metrics.fdr_ratio,
                bopo_ratio=current_metrics.bopo_ratio,
                roa=current_metrics.roa * (1 + adjustments.get('profitability_shock', 0)),
                roe=current_metrics.roe * (1 + adjustments.get('profitability_shock', 0)),
                liquidity_ratio=current_metrics.liquidity_ratio,
                concentration_risk=current_metrics.concentration_risk,
                market_share=current_metrics.market_share,
                gdp_growth=current_metrics.gdp_growth + adjustments.get('gdp_shock', 0),
                inflation_rate=current_metrics.inflation_rate + adjustments.get('inflation_shock', 0),
                bi_rate=current_metrics.bi_rate + adjustments.get('rate_shock', 0)
            )
            
            # Calculate stressed PD
            stressed_pd = self.calculate_pd(stressed_metrics)
            
            # Calculate impact
            results[scenario_name] = {
                'stressed_npf': stressed_metrics.npf_ratio,
                'stressed_pd': stressed_pd,
                'capital_impact': self._calculate_capital_impact(
                    stressed_metrics.npf_ratio,
                    current_metrics.car_ratio
                ),
                'risk_rating': self._get_risk_rating(stressed_metrics.npf_ratio)
            }
            
        return results
        
    def _calculate_capital_impact(self, npf: float, current_car: float) -> float:
        """Calculate impact on capital from NPF increase"""
        # Simplified calculation
        provision_rate = min(1.0, npf / 5.0)  # Progressive provisioning
        capital_erosion = npf * provision_rate * 0.5  # Assume 50% capital impact
        
        new_car = current_car - capital_erosion
        return new_car
        
    def _get_risk_rating(self, npf: float) -> str:
        """Get risk rating based on NPF level"""
        if npf >= self.risk_thresholds['critical']:
            return 'CRITICAL'
        elif npf >= self.risk_thresholds['high']:
            return 'HIGH'
        elif npf >= self.risk_thresholds['medium']:
            return 'MEDIUM'
        else:
            return 'LOW'
            
    def calculate_portfolio_var(
        self,
        portfolio_data: pd.DataFrame,
        confidence_level: float = 0.99,
        time_horizon: int = 10
    ) -> Dict[str, float]:
        """
        Calculate Value at Risk for loan portfolio
        """
        if portfolio_data.empty:
            # Use mock data for demonstration
            portfolio_value = 22_500_000_000_000  # 22.5 trillion IDR
            portfolio_std = 0.05  # 5% standard deviation
        else:
            portfolio_value = portfolio_data['exposure'].sum()
            portfolio_std = portfolio_data['exposure'].std() / portfolio_value
            
        # Calculate VaR using parametric method
        z_score = 2.33 if confidence_level == 0.99 else 1.96  # 99% or 95% confidence
        
        # Daily VaR
        daily_var = portfolio_value * portfolio_std * z_score / np.sqrt(252)
        
        # Scale to time horizon
        var = daily_var * np.sqrt(time_horizon)
        
        # Calculate Expected Shortfall (CVaR)
        es = var * 1.4  # Approximation for normal distribution
        
        return {
            'var': var,
            'var_percentage': (var / portfolio_value) * 100,
            'expected_shortfall': es,
            'es_percentage': (es / portfolio_value) * 100,
            'confidence_level': confidence_level,
            'time_horizon': time_horizon
        }

class OperationalRiskModel:
    """
    Operational risk model using Advanced Measurement Approach (AMA)
    """
    
    def __init__(self):
        self.risk_categories = {
            'internal_fraud': 0.1,
            'external_fraud': 0.15,
            'employment_practices': 0.05,
            'clients_products': 0.2,
            'damage_assets': 0.05,
            'business_disruption': 0.25,
            'execution_delivery': 0.2
        }
        
    def calculate_operational_var(
        self,
        gross_income: float,
        loss_history: Optional[pd.DataFrame] = None
    ) -> Dict[str, float]:
        """
        Calculate operational risk VaR using Basic Indicator Approach
        """
        # Basic Indicator Approach: 15% of average gross income
        bia_capital = gross_income * 0.15
        
        if loss_history is not None and not loss_history.empty:
            # Use historical loss data if available
            loss_severity = loss_history['loss_amount'].mean()
            loss_frequency = len(loss_history) / loss_history['year'].nunique()
            
            # Simple frequency-severity model
            annual_expected_loss = loss_severity * loss_frequency
            unexpected_loss = annual_expected_loss * 2.5  # Stress multiplier
            
            operational_var = max(bia_capital, unexpected_loss)
        else:
            operational_var = bia_capital
            
        return {
            'operational_var': operational_var,
            'bia_capital': bia_capital,
            'risk_capital_ratio': (operational_var / gross_income) * 100
        }
        
    def assess_control_effectiveness(
        self,
        control_scores: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Assess effectiveness of operational controls
        """
        overall_score = np.mean(list(control_scores.values()))
        
        effectiveness = {
            'overall_score': overall_score,
            'rating': self._get_control_rating(overall_score),
            'weak_controls': [
                control for control, score in control_scores.items()
                if score < 0.6
            ],
            'strong_controls': [
                control for control, score in control_scores.items()
                if score >= 0.8
            ]
        }
        
        return effectiveness
        
    def _get_control_rating(self, score: float) -> str:
        """Get control effectiveness rating"""
        if score >= 0.8:
            return 'STRONG'
        elif score >= 0.6:
            return 'ADEQUATE'
        elif score >= 0.4:
            return 'NEEDS_IMPROVEMENT'
        else:
            return 'WEAK'

class MarketRiskModel:
    """
    Market risk model for profit rate risk and FX risk
    """
    
    def __init__(self):
        self.duration_buckets = {
            '0-1M': 0.08,
            '1-3M': 0.25,
            '3-6M': 0.5,
            '6-12M': 1.0,
            '1-3Y': 2.0,
            '3-5Y': 4.0,
            '>5Y': 6.0
        }
        
    def calculate_profit_rate_risk(
        self,
        assets_by_maturity: Dict[str, float],
        liabilities_by_maturity: Dict[str, float],
        rate_shock: float = 0.02  # 200 bps
    ) -> Dict[str, float]:
        """
        Calculate profit rate risk in banking book
        """
        total_assets = sum(assets_by_maturity.values())
        total_liabilities = sum(liabilities_by_maturity.values())
        
        # Calculate duration-weighted positions
        asset_duration = sum(
            assets_by_maturity.get(bucket, 0) * duration
            for bucket, duration in self.duration_buckets.items()
        ) / total_assets if total_assets > 0 else 0
        
        liability_duration = sum(
            liabilities_by_maturity.get(bucket, 0) * duration
            for bucket, duration in self.duration_buckets.items()
        ) / total_liabilities if total_liabilities > 0 else 0
        
        # Duration gap
        duration_gap = asset_duration - liability_duration
        
        # Economic value impact
        eva_impact = duration_gap * rate_shock * total_assets
        
        # Net interest income impact (simplified)
        nii_impact = (total_assets - total_liabilities) * rate_shock
        
        return {
            'duration_gap': duration_gap,
            'eva_impact': eva_impact,
            'eva_impact_percentage': (eva_impact / total_assets) * 100,
            'nii_impact': nii_impact,
            'rate_sensitivity': 'ASSET_SENSITIVE' if duration_gap > 0 else 'LIABILITY_SENSITIVE'
        }
        
    def calculate_fx_risk(
        self,
        fx_positions: Dict[str, float],
        fx_volatilities: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Calculate foreign exchange risk
        """
        # Calculate net open position
        net_position = sum(fx_positions.values())
        
        # Calculate VaR for each currency
        fx_vars = {}
        for currency, position in fx_positions.items():
            volatility = fx_volatilities.get(currency, 0.1)  # Default 10% volatility
            fx_vars[currency] = abs(position) * volatility * 2.33  # 99% confidence
            
        # Total FX VaR (assuming no correlation)
        total_fx_var = np.sqrt(sum(var ** 2 for var in fx_vars.values()))
        
        return {
            'net_open_position': net_position,
            'fx_var': total_fx_var,
            'currency_vars': fx_vars,
            'largest_exposure': max(fx_positions.items(), key=lambda x: abs(x[1]))
        }

class LiquidityRiskModel:
    """
    Liquidity risk model for Islamic banks
    """
    
    def __init__(self):
        self.runoff_rates = {
            'stable_deposits': 0.05,
            'less_stable_deposits': 0.10,
            'corporate_deposits': 0.40,
            'interbank': 0.100
        }
        
    def calculate_lcr(
        self,
        hqla: float,
        cash_outflows: Dict[str, float],
        cash_inflows: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Calculate Liquidity Coverage Ratio
        """
        # Calculate weighted outflows
        total_outflows = sum(
            amount * self.runoff_rates.get(category, 1.0)
            for category, amount in cash_outflows.items()
        )
        
        # Calculate inflows (capped at 75% of outflows)
        total_inflows = min(
            sum(cash_inflows.values()),
            0.75 * total_outflows
        )
        
        # Net cash outflows
        net_outflows = total_outflows - total_inflows
        
        # LCR calculation
        lcr = (hqla / net_outflows * 100) if net_outflows > 0 else 999
        
        return {
            'lcr': min(lcr, 999),  # Cap at 999%
            'hqla': hqla,
            'net_outflows': net_outflows,
            'total_outflows': total_outflows,
            'total_inflows': total_inflows,
            'lcr_requirement': 100,
            'buffer': lcr - 100,
            'compliant': lcr >= 100
        }
        
    def calculate_nsfr(
        self,
        available_stable_funding: Dict[str, float],
        required_stable_funding: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Calculate Net Stable Funding Ratio
        """
        # ASF factors
        asf_factors = {
            'capital': 1.0,
            'stable_deposits': 0.95,
            'less_stable_deposits': 0.90,
            'wholesale_funding': 0.50
        }
        
        # RSF factors
        rsf_factors = {
            'cash': 0.0,
            'securities': 0.15,
            'retail_loans': 0.65,
            'corporate_loans': 0.85,
            'other_assets': 1.0
        }
        
        # Calculate weighted ASF
        total_asf = sum(
            amount * asf_factors.get(category, 0)
            for category, amount in available_stable_funding.items()
        )
        
        # Calculate weighted RSF
        total_rsf = sum(
            amount * rsf_factors.get(category, 1.0)
            for category, amount in required_stable_funding.items()
        )
        
        # NSFR calculation
        nsfr = (total_asf / total_rsf * 100) if total_rsf > 0 else 999
        
        return {
            'nsfr': min(nsfr, 999),
            'available_stable_funding': total_asf,
            'required_stable_funding': total_rsf,
            'nsfr_requirement': 100,
            'buffer': nsfr - 100,
            'compliant': nsfr >= 100
        }
        
    def stress_test_liquidity(
        self,
        current_lcr: float,
        deposit_base: float,
        stress_scenarios: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Perform liquidity stress testing
        """
        results = {}
        
        for scenario, runoff_multiplier in stress_scenarios.items():
            # Calculate stressed deposit runoff
            stressed_runoff = deposit_base * runoff_multiplier
            
            # Impact on LCR (simplified)
            lcr_impact = current_lcr * (1 - runoff_multiplier)
            
            # Survival period (days)
            survival_days = int(30 * (lcr_impact / 100)) if lcr_impact > 0 else 0
            
            results[scenario] = {
                'stressed_lcr': max(0, lcr_impact),
                'deposit_runoff': stressed_runoff,
                'survival_period_days': survival_days,
                'severity': self._get_severity(lcr_impact)
            }
            
        return results
        
    def _get_severity(self, lcr: float) -> str:
        """Get severity level based on stressed LCR"""
        if lcr >= 100:
            return 'LOW'
        elif lcr >= 80:
            return 'MEDIUM'
        elif lcr >= 60:
            return 'HIGH'
        else:
            return 'CRITICAL'

class IntegratedRiskModel:
    """
    Integrated risk model combining all risk types
    """
    
    def __init__(self):
        self.credit_risk_model = CreditRiskModel()
        self.operational_risk_model = OperationalRiskModel()
        self.market_risk_model = MarketRiskModel()
        self.liquidity_risk_model = LiquidityRiskModel()
        
    def calculate_economic_capital(
        self,
        risk_metrics: RiskMetrics,
        portfolio_data: pd.DataFrame,
        confidence_level: float = 0.99
    ) -> Dict[str, Any]:
        """
        Calculate total economic capital requirements
        """
        # Credit risk capital
        credit_var = self.credit_risk_model.calculate_portfolio_var(
            portfolio_data,
            confidence_level
        )
        
        # Operational risk capital
        operational_var = self.operational_risk_model.calculate_operational_var(
            gross_income=1_000_000_000_000  # 1 trillion IDR mock
        )
        
        # Market risk capital (simplified)
        market_risk_capital = risk_metrics.car_ratio * 0.1  # 10% of CAR
        
        # Total economic capital (assuming correlation)
        correlation_factor = 0.3  # Inter-risk correlation
        
        total_ec = np.sqrt(
            credit_var['var'] ** 2 +
            operational_var['operational_var'] ** 2 +
            market_risk_capital ** 2 +
            2 * correlation_factor * credit_var['var'] * operational_var['operational_var']
        )
        
        return {
            'total_economic_capital': total_ec,
            'credit_risk_capital': credit_var['var'],
            'operational_risk_capital': operational_var['operational_var'],
            'market_risk_capital': market_risk_capital,
            'capital_adequacy': (risk_metrics.car_ratio * 1e13) / total_ec,  # Assuming CAR in trillions
            'capital_buffer': (risk_metrics.car_ratio * 1e13) - total_ec
        }
        
    def generate_risk_dashboard(
        self,
        risk_metrics: RiskMetrics
    ) -> Dict[str, Any]:
        """
        Generate comprehensive risk dashboard
        """
        # Calculate individual risk scores
        credit_score = self._calculate_credit_score(risk_metrics)
        operational_score = self._calculate_operational_score(risk_metrics)
        market_score = self._calculate_market_score(risk_metrics)
        liquidity_score = self._calculate_liquidity_score(risk_metrics)
        
        # Weighted composite score
        weights = {
            'credit': 0.4,
            'operational': 0.2,
            'market': 0.2,
            'liquidity': 0.2
        }
        
        composite_score = (
            credit_score * weights['credit'] +
            operational_score * weights['operational'] +
            market_score * weights['market'] +
            liquidity_score * weights['liquidity']
        )
        
        return {
            'composite_risk_score': round(composite_score, 2),
            'risk_rating': self._get_overall_rating(composite_score),
            'individual_scores': {
                'credit': credit_score,
                'operational': operational_score,
                'market': market_score,
                'liquidity': liquidity_score
            },
            'risk_appetite_status': self._check_risk_appetite(composite_score),
            'key_risk_indicators': self._get_key_risk_indicators(risk_metrics),
            'action_required': composite_score < 60
        }
        
    def _calculate_credit_score(self, metrics: RiskMetrics) -> float:
        """Calculate credit risk score (0-100, higher is better)"""
        npf_score = max(0, 100 - (metrics.npf_ratio / 5.0) * 100)
        car_score = min(100, (metrics.car_ratio / 15.0) * 100)
        
        return 0.7 * npf_score + 0.3 * car_score
        
    def _calculate_operational_score(self, metrics: RiskMetrics) -> float:
        """Calculate operational risk score"""
        bopo_score = max(0, 100 - ((metrics.bopo_ratio - 50) / 50) * 100)
        return bopo_score
        
    def _calculate_market_score(self, metrics: RiskMetrics) -> float:
        """Calculate market risk score"""
        # Simplified scoring based on FDR
        fdr_score = 100 - abs(metrics.fdr_ratio - 85) * 2  # Optimal around 85%
        return max(0, min(100, fdr_score))
        
    def _calculate_liquidity_score(self, metrics: RiskMetrics) -> float:
        """Calculate liquidity risk score"""
        liquidity_score = min(100, metrics.liquidity_ratio)
        fdr_penalty = max(0, (metrics.fdr_ratio - 100) * 2)
        
        return max(0, liquidity_score - fdr_penalty)
        
    def _get_overall_rating(self, score: float) -> str:
        """Get overall risk rating"""
        if score >= 80:
            return 'LOW_RISK'
        elif score >= 60:
            return 'MODERATE_RISK'
        elif score >= 40:
            return 'HIGH_RISK'
        else:
            return 'CRITICAL_RISK'
            
    def _check_risk_appetite(self, score: float) -> str:
        """Check against risk appetite"""
        if score >= 70:
            return 'WITHIN_APPETITE'
        elif score >= 50:
            return 'APPROACHING_LIMIT'
        else:
            return 'EXCEEDS_APPETITE'
            
    def _get_key_risk_indicators(self, metrics: RiskMetrics) -> List[Dict[str, Any]]:
        """Get key risk indicators with status"""
        return [
            {
                'indicator': 'NPF Ratio',
                'value': metrics.npf_ratio,
                'threshold': 5.0,
                'status': 'BREACH' if metrics.npf_ratio > 5.0 else 'WARNING' if metrics.npf_ratio > 3.0 else 'NORMAL'
            },
            {
                'indicator': 'CAR',
                'value': metrics.car_ratio,
                'threshold': 12.0,
                'status': 'NORMAL' if metrics.car_ratio > 15.0 else 'WARNING' if metrics.car_ratio > 12.0 else 'BREACH'
            },
            {
                'indicator': 'BOPO',
                'value': metrics.bopo_ratio,
                'threshold': 85.0,
                'status': 'BREACH' if metrics.bopo_ratio > 95.0 else 'WARNING' if metrics.bopo_ratio > 85.0 else 'NORMAL'
            },
            {
                'indicator': 'FDR',
                'value': metrics.fdr_ratio,
                'threshold': 92.0,
                'status': 'WARNING' if metrics.fdr_ratio > 92.0 or metrics.fdr_ratio < 75.0 else 'NORMAL'
            }
        ]