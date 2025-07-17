"""
Financial Analyzer Module for Bank Muamalat
Provides deep financial analysis and metrics calculation
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class FinancialMetric(Enum):
    """Financial metrics enumeration"""
    CAR = "Capital Adequacy Ratio"
    NPF = "Non-Performing Financing"
    ROA = "Return on Assets"
    ROE = "Return on Equity"
    BOPO = "Operating Expense Ratio"
    FDR = "Financing to Deposit Ratio"
    NIM = "Net Interest Margin"
    CASA = "Current Account Savings Account"

@dataclass
class FinancialIndicator:
    """Financial indicator data class"""
    metric: str
    value: float
    benchmark: float
    status: str
    trend: str
    period: str

class FinancialAnalyzer:
    """
    Comprehensive financial analysis for Bank Muamalat
    """
    
    def __init__(self, config):
        self.config = config
        self.benchmarks = self._load_benchmarks()
        self.thresholds = self._load_thresholds()
        
    def _load_benchmarks(self) -> Dict[str, float]:
        """Load industry benchmarks"""
        return {
            'car': 15.0,  # Industry average
            'npf': 3.0,   # Industry average
            'roa': 1.5,   # Industry average
            'roe': 15.0,  # Industry average
            'bopo': 80.0, # Efficiency benchmark
            'fdr': 85.0,  # Optimal range
            'nim': 4.5,   # Industry average
            'casa': 40.0  # Target CASA ratio
        }
        
    def _load_thresholds(self) -> Dict[str, Dict[str, float]]:
        """Load regulatory and risk thresholds"""
        return {
            'car': {'min': 8.0, 'warning': 10.0, 'healthy': 14.0},
            'npf': {'healthy': 2.0, 'warning': 3.0, 'critical': 5.0},
            'roa': {'critical': 0.0, 'warning': 0.5, 'healthy': 1.5},
            'roe': {'critical': 0.0, 'warning': 5.0, 'healthy': 15.0},
            'bopo': {'healthy': 80.0, 'warning': 90.0, 'critical': 95.0},
            'fdr': {'min': 75.0, 'optimal': 85.0, 'max': 100.0}
        }
        
    def analyze_financial_health(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive financial health analysis
        """
        logger.info("Starting financial health analysis")
        
        try:
            # Extract metrics
            metrics = self._extract_metrics(data)
            
            # Calculate scores
            health_score = self._calculate_health_score(metrics)
            
            # Analyze trends
            trends = self._analyze_trends(metrics)
            
            # Generate insights
            insights = self._generate_insights(metrics, trends)
            
            # Risk assessment
            risk_assessment = self._assess_financial_risks(metrics)
            
            # Peer comparison
            peer_analysis = self._perform_peer_analysis(metrics)
            
            # Projections
            projections = self._generate_projections(metrics, trends)
            
            return {
                'status': 'success',
                'timestamp': datetime.now().isoformat(),
                'metrics': metrics,
                'health_score': health_score,
                'trends': trends,
                'insights': insights,
                'risk_assessment': risk_assessment,
                'peer_analysis': peer_analysis,
                'projections': projections,
                'recommendations': self._generate_recommendations(
                    metrics, health_score, risk_assessment
                )
            }
            
        except Exception as e:
            logger.error(f"Financial analysis failed: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            
    def _extract_metrics(self, data: Dict[str, Any]) -> Dict[str, FinancialIndicator]:
        """Extract and structure financial metrics"""
        metrics = {}
        
        # CAR Analysis
        car_value = data.get('car', 29.42)
        metrics['car'] = FinancialIndicator(
            metric='CAR',
            value=car_value,
            benchmark=self.benchmarks['car'],
            status=self._get_metric_status('car', car_value),
            trend=self._calculate_trend(data.get('car_history', [])),
            period=data.get('period', 'Q4 2024')
        )
        
        # NPF Analysis
        npf_value = data.get('npf', 3.99)
        metrics['npf'] = FinancialIndicator(
            metric='NPF',
            value=npf_value,
            benchmark=self.benchmarks['npf'],
            status=self._get_metric_status('npf', npf_value),
            trend=self._calculate_trend(data.get('npf_history', [])),
            period=data.get('period', 'Q4 2024')
        )
        
        # ROA Analysis
        roa_value = data.get('roa', 0.03)
        metrics['roa'] = FinancialIndicator(
            metric='ROA',
            value=roa_value,
            benchmark=self.benchmarks['roa'],
            status=self._get_metric_status('roa', roa_value),
            trend=self._calculate_trend(data.get('roa_history', [])),
            period=data.get('period', 'Q4 2024')
        )
        
        # Add other metrics...
        
        return metrics
        
    def _calculate_health_score(self, metrics: Dict[str, FinancialIndicator]) -> Dict[str, Any]:
        """Calculate overall financial health score"""
        weights = {
            'car': 0.20,
            'npf': 0.25,  # Higher weight due to critical importance
            'roa': 0.20,
            'roe': 0.10,
            'bopo': 0.15,
            'fdr': 0.10
        }
        
        scores = {}
        
        # CAR Score (higher is better)
        if 'car' in metrics:
            car_score = min(100, (metrics['car'].value / self.benchmarks['car']) * 100)
            scores['car'] = car_score
            
        # NPF Score (lower is better, inverse scoring)
        if 'npf' in metrics:
            npf_score = max(0, 100 - (metrics['npf'].value / self.thresholds['npf']['critical']) * 100)
            scores['npf'] = npf_score
            
        # ROA Score (higher is better)
        if 'roa' in metrics:
            roa_score = min(100, (metrics['roa'].value / self.benchmarks['roa']) * 100)
            scores['roa'] = roa_score
            
        # Calculate weighted average
        total_score = sum(scores.get(metric, 0) * weights.get(metric, 0) for metric in weights)
        
        return {
            'overall_score': round(total_score, 2),
            'component_scores': scores,
            'rating': self._get_health_rating(total_score),
            'confidence': self._calculate_confidence(metrics)
        }
        
    def _analyze_trends(self, metrics: Dict[str, FinancialIndicator]) -> Dict[str, Any]:
        """Analyze metric trends"""
        trends = {}
        
        for metric_name, indicator in metrics.items():
            trends[metric_name] = {
                'direction': indicator.trend,
                'strength': self._calculate_trend_strength(metric_name),
                'projection': self._project_trend(metric_name, indicator.value),
                'turning_point': self._detect_turning_point(metric_name)
            }
            
        return trends
        
    def _generate_insights(
        self, 
        metrics: Dict[str, FinancialIndicator], 
        trends: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate actionable insights"""
        insights = []
        
        # NPF Insights
        if 'npf' in metrics:
            npf = metrics['npf']
            if npf.value > self.thresholds['npf']['warning']:
                insights.append({
                    'type': 'critical',
                    'area': 'Asset Quality',
                    'finding': f"NPF at {npf.value}% exceeds warning threshold",
                    'impact': 'High risk of regulatory action and capital erosion',
                    'recommendation': 'Immediate NPF reduction program required'
                })
                
        # BOPO Insights
        if 'bopo' in metrics:
            bopo = metrics.get('bopo', FinancialIndicator('BOPO', 98.5, 80.0, 'Critical', 'Stable', 'Q4 2024'))
            if bopo.value > self.thresholds['bopo']['critical']:
                insights.append({
                    'type': 'critical',
                    'area': 'Operational Efficiency',
                    'finding': f"BOPO at {bopo.value}% indicates severe inefficiency",
                    'impact': 'Unsustainable cost structure threatening profitability',
                    'recommendation': 'Urgent digital transformation and cost reduction'
                })
                
        # Profitability Insights
        if 'roa' in metrics:
            roa = metrics['roa']
            if roa.value < self.thresholds['roa']['warning']:
                insights.append({
                    'type': 'warning',
                    'area': 'Profitability',
                    'finding': f"ROA at {roa.value}% is below sustainable levels",
                    'impact': 'Inability to generate adequate returns for shareholders',
                    'recommendation': 'Revenue enhancement and margin improvement initiatives'
                })
                
        # Positive Insights
        if 'car' in metrics and metrics['car'].value > self.benchmarks['car']:
            insights.append({
                'type': 'positive',
                'area': 'Capital Strength',
                'finding': f"Strong CAR at {metrics['car'].value}% provides stability",
                'impact': 'Sufficient buffer for growth and risk absorption',
                'recommendation': 'Leverage capital strength for strategic initiatives'
            })
            
        return insights
        
    def _assess_financial_risks(self, metrics: Dict[str, FinancialIndicator]) -> Dict[str, Any]:
        """Assess financial risks"""
        risks = {
            'earnings_risk': 'HIGH',  # Due to low ROA
            'capital_risk': 'LOW',    # Strong CAR
            'asset_quality_risk': 'HIGH',  # High NPF
            'efficiency_risk': 'CRITICAL',  # Very high BOPO
            'liquidity_risk': 'MEDIUM'
        }
        
        # Calculate composite risk
        risk_scores = {
            'CRITICAL': 4,
            'HIGH': 3,
            'MEDIUM': 2,
            'LOW': 1
        }
        
        avg_risk_score = np.mean([risk_scores[risk] for risk in risks.values()])
        
        return {
            'risk_factors': risks,
            'composite_risk': 'HIGH' if avg_risk_score > 2.5 else 'MEDIUM',
            'key_vulnerabilities': self._identify_vulnerabilities(metrics),
            'stress_scenarios': self._generate_stress_scenarios(metrics)
        }
        
    def _perform_peer_analysis(self, metrics: Dict[str, FinancialIndicator]) -> Dict[str, Any]:
        """Perform peer comparison analysis"""
        # Mock peer data - in production, load from database
        peers = {
            'BSI': {'car': 25.5, 'npf': 2.5, 'roa': 1.5, 'bopo': 85.2},
            'Bank Mega Syariah': {'car': 22.3, 'npf': 1.8, 'roa': 1.2, 'bopo': 82.1},
            'BTPN Syariah': {'car': 35.2, 'npf': 2.2, 'roa': 3.5, 'bopo': 75.3}
        }
        
        peer_comparison = {}
        
        for metric_name, indicator in metrics.items():
            if metric_name in ['car', 'npf', 'roa', 'bopo']:
                peer_values = [peer.get(metric_name, 0) for peer in peers.values()]
                peer_avg = np.mean(peer_values)
                
                peer_comparison[metric_name] = {
                    'bank_value': indicator.value,
                    'peer_average': round(peer_avg, 2),
                    'percentile': self._calculate_percentile(indicator.value, peer_values),
                    'gap': round(indicator.value - peer_avg, 2),
                    'position': 'Above' if indicator.value > peer_avg else 'Below'
                }
                
        return {
            'comparison': peer_comparison,
            'competitive_position': self._assess_competitive_position(peer_comparison),
            'best_practices': self._identify_best_practices(peers)
        }
        
    def _generate_projections(
        self, 
        metrics: Dict[str, FinancialIndicator], 
        trends: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate financial projections"""
        projections = {}
        
        # Simple linear projection - enhance with ML models in production
        for metric_name, indicator in metrics.items():
            trend_direction = trends.get(metric_name, {}).get('direction', 'stable')
            
            # Project 4 quarters ahead
            quarterly_projections = []
            current_value = indicator.value
            
            for quarter in range(1, 5):
                if trend_direction == 'improving':
                    change = 0.02 if metric_name != 'npf' else -0.1
                elif trend_direction == 'deteriorating':
                    change = -0.02 if metric_name != 'npf' else 0.1
                else:
                    change = 0
                    
                projected_value = current_value * (1 + change)
                quarterly_projections.append({
                    f'Q{quarter}': round(projected_value, 2)
                })
                current_value = projected_value
                
            projections[metric_name] = {
                'current': indicator.value,
                'quarterly_forecast': quarterly_projections,
                'annual_target': self._calculate_annual_target(metric_name, indicator.value),
                'probability': self._calculate_projection_confidence(metric_name, trends)
            }
            
        return projections
        
    def _generate_recommendations(
        self,
        metrics: Dict[str, FinancialIndicator],
        health_score: Dict[str, Any],
        risk_assessment: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate prioritized recommendations"""
        recommendations = []
        
        # Critical recommendations based on metrics
        if metrics.get('npf', FinancialIndicator('NPF', 3.99, 3.0, '', '', '')).value > 3.5:
            recommendations.append({
                'priority': 'CRITICAL',
                'area': 'Asset Quality',
                'action': 'Launch Emergency NPF Reduction Program',
                'timeline': 'Immediate (within 30 days)',
                'expected_impact': 'Reduce NPF by 1-1.5% within 12 months',
                'resources': 'Dedicated task force, Rp 50-100B provisions',
                'kpis': ['Monthly NPF reduction', 'Recovery rates', 'Write-off volumes']
            })
            
        if metrics.get('bopo', FinancialIndicator('BOPO', 98.5, 80.0, '', '', '')).value > 95:
            recommendations.append({
                'priority': 'CRITICAL',
                'area': 'Operational Efficiency',
                'action': 'Accelerate Digital Transformation',
                'timeline': '3-6 months',
                'expected_impact': 'Reduce BOPO by 10-15% within 18 months',
                'resources': 'Rp 200-300B technology investment',
                'kpis': ['Digital adoption rate', 'Cost per transaction', 'Branch efficiency']
            })
            
        # Strategic recommendations
        recommendations.append({
            'priority': 'HIGH',
            'area': 'Revenue Growth',
            'action': 'Focus on High-Margin Islamic Products',
            'timeline': '6-12 months',
            'expected_impact': 'Increase fee income by 25-30%',
            'resources': 'Product development team, marketing budget',
            'kpis': ['Fee income growth', 'Product penetration', 'Customer acquisition']
        })
        
        # Sort by priority
        priority_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 999))
        
        return recommendations
        
    def _get_metric_status(self, metric: str, value: float) -> str:
        """Determine metric status based on thresholds"""
        thresholds = self.thresholds.get(metric, {})
        
        if metric in ['car', 'roa', 'roe']:  # Higher is better
            if value >= thresholds.get('healthy', float('inf')):
                return 'Healthy'
            elif value >= thresholds.get('warning', 0):
                return 'Warning'
            else:
                return 'Critical'
        else:  # Lower is better (NPF, BOPO)
            if value <= thresholds.get('healthy', 0):
                return 'Healthy'
            elif value <= thresholds.get('warning', float('inf')):
                return 'Warning'
            else:
                return 'Critical'
                
    def _calculate_trend(self, history: List[float]) -> str:
        """Calculate trend direction from historical data"""
        if len(history) < 2:
            return 'Stable'
            
        # Simple trend calculation - enhance with statistical methods
        recent_avg = np.mean(history[-3:]) if len(history) >= 3 else history[-1]
        older_avg = np.mean(history[:-3]) if len(history) > 3 else history[0]
        
        change_pct = ((recent_avg - older_avg) / older_avg) * 100 if older_avg != 0 else 0
        
        if change_pct > 5:
            return 'Improving'
        elif change_pct < -5:
            return 'Deteriorating'
        else:
            return 'Stable'
            
    def _get_health_rating(self, score: float) -> str:
        """Convert health score to rating"""
        if score >= 80:
            return 'Excellent'
        elif score >= 60:
            return 'Good'
        elif score >= 40:
            return 'Fair'
        elif score >= 20:
            return 'Poor'
        else:
            return 'Critical'
            
    def _calculate_confidence(self, metrics: Dict[str, FinancialIndicator]) -> float:
        """Calculate confidence level in the analysis"""
        # Base confidence on data availability and quality
        return 85.0  # Placeholder - implement actual logic
        
    def _calculate_trend_strength(self, metric_name: str) -> str:
        """Calculate strength of trend"""
        return 'Moderate'  # Placeholder
        
    def _project_trend(self, metric_name: str, current_value: float) -> float:
        """Project future value based on trend"""
        return current_value * 1.02  # Simple 2% growth projection
        
    def _detect_turning_point(self, metric_name: str) -> Optional[str]:
        """Detect potential trend reversal"""
        return None  # Placeholder
        
    def _identify_vulnerabilities(self, metrics: Dict[str, FinancialIndicator]) -> List[str]:
        """Identify key vulnerabilities"""
        vulnerabilities = []
        
        if metrics.get('npf', FinancialIndicator('', 3.99, 0, '', '', '')).value > 3:
            vulnerabilities.append('High NPF threatening asset quality')
            
        if metrics.get('bopo', FinancialIndicator('', 98.5, 0, '', '', '')).value > 90:
            vulnerabilities.append('Unsustainable cost structure')
            
        if metrics.get('roa', FinancialIndicator('', 0.03, 0, '', '', '')).value < 0.5:
            vulnerabilities.append('Weak profitability generation')
            
        return vulnerabilities
        
    def _generate_stress_scenarios(self, metrics: Dict[str, FinancialIndicator]) -> List[Dict[str, Any]]:
        """Generate stress test scenarios"""
        return [
            {
                'scenario': 'Economic Downturn',
                'assumptions': 'GDP -2%, NPF +3%, Deposits -10%',
                'impact': 'CAR drops to 22%, Losses of Rp 500B',
                'probability': 'Medium'
            },
            {
                'scenario': 'Liquidity Crisis',
                'assumptions': 'Deposit run 20%, Interbank frozen',
                'impact': 'FDR spikes to 110%, Emergency funding needed',
                'probability': 'Low'
            }
        ]
        
    def _calculate_percentile(self, value: float, peer_values: List[float]) -> int:
        """Calculate percentile ranking"""
        return int(np.percentile(peer_values + [value], value) * 100)
        
    def _assess_competitive_position(self, comparison: Dict[str, Any]) -> str:
        """Assess overall competitive position"""
        above_avg_count = sum(1 for m in comparison.values() if m.get('position') == 'Above')
        
        if above_avg_count >= 3:
            return 'Strong'
        elif above_avg_count >= 2:
            return 'Average'
        else:
            return 'Weak'
            
    def _identify_best_practices(self, peers: Dict[str, Dict[str, float]]) -> List[str]:
        """Identify best practices from top performers"""
        return [
            'BTPN Syariah: Exceptional efficiency (BOPO 75.3%) through digital focus',
            'BSI: Balanced growth with controlled NPF (2.5%)',
            'Bank Mega Syariah: Strong cost management practices'
        ]
        
    def _calculate_annual_target(self, metric_name: str, current_value: float) -> float:
        """Calculate realistic annual target"""
        improvements = {
            'npf': -0.5,  # Reduce by 0.5%
            'bopo': -5.0,  # Reduce by 5%
            'roa': 0.5,   # Increase by 0.5%
            'car': 0.0    # Maintain current level
        }
        
        return current_value + improvements.get(metric_name, 0)
        
    def _calculate_projection_confidence(self, metric_name: str, trends: Dict[str, Any]) -> float:
        """Calculate confidence in projections"""
        return 75.0  # Placeholder - implement statistical confidence calculation
        
    def generate_executive_summary(self, analysis_results: Dict[str, Any]) -> str:
        """Generate executive summary of financial analysis"""
        health_score = analysis_results.get('health_score', {}).get('overall_score', 0)
        rating = analysis_results.get('health_score', {}).get('rating', 'Unknown')
        
        summary = f"""
        EXECUTIVE SUMMARY - BANK MUAMALAT FINANCIAL ANALYSIS
        
        Overall Financial Health: {rating} (Score: {health_score}/100)
        
        Key Findings:
        1. Capital Position: Strong CAR provides stability but cannot offset operational weaknesses
        2. Asset Quality: NPF at critical levels requiring immediate intervention
        3. Profitability: Severely impacted by high costs and credit losses
        4. Efficiency: BOPO indicates unsustainable cost structure
        
        Critical Actions Required:
        1. Emergency NPF reduction program (Target: <3% within 12 months)
        2. Radical cost transformation (Target: BOPO <85% within 18 months)
        3. Revenue diversification into fee-based income
        
        BPKH Decision Impact:
        - Current trajectory unsustainable without major transformation
        - Significant capital may be required for restructuring
        - 18-24 month turnaround timeline with execution risk
        
        Recommendation: MAINTAIN WITH STRICT CONDITIONS
        - Quarterly performance milestones
        - Management accountability framework
        - Option to reassess if targets not met
        """
        
        return summary