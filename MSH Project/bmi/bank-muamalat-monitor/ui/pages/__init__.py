"""
Pages package for Bank Muamalat Health Monitoring UI
"""

# Import all page modules
from . import overview
from . import financial_health
from . import risk_assessment
from . import compliance_monitoring
from . import strategic_analysis
from . import decision_support

# Export all modules
__all__ = [
    'overview',
    'financial_health',
    'risk_assessment',
    'compliance_monitoring',
    'strategic_analysis',
    'decision_support'
]