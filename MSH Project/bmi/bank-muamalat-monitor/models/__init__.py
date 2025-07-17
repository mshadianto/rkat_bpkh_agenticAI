"""
Models package for Bank Muamalat Health Monitoring System
Contains data models, metrics, and prediction models
"""

from .bank_metrics import (
    BankMetrics,
    FinancialRatios,
    RiskIndicators,
    PerformanceMetrics,
    ComplianceMetrics
)

from .risk_models import (
    RiskScoreModel,
    NPFPredictionModel,
    EarlyWarningModel,
    StressTestModel,
    RiskMatrix
)

from .prediction_models import (
    FinancialForecastModel,
    NPFTrendPredictor,
    ProfitabilityPredictor,
    LiquidityPredictor,
    HealthScorePredictor
)

__all__ = [
    # Bank Metrics
    'BankMetrics',
    'FinancialRatios',
    'RiskIndicators',
    'PerformanceMetrics',
    'ComplianceMetrics',
    
    # Risk Models
    'RiskScoreModel',
    'NPFPredictionModel',
    'EarlyWarningModel',
    'StressTestModel',
    'RiskMatrix',
    
    # Prediction Models
    'FinancialForecastModel',
    'NPFTrendPredictor',
    'ProfitabilityPredictor',
    'LiquidityPredictor',
    'HealthScorePredictor'
]

# Version info
__version__ = '1.0.0'
__author__ = 'BPKH Analytics Team'