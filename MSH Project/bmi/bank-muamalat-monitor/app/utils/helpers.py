"""
Helper functions and utilities for Bank Muamalat Health Monitor
"""

import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Tuple
import pandas as pd
import numpy as np
from pathlib import Path
import re
import os
from functools import wraps, lru_cache
import time

def format_currency(amount: float, currency: str = "IDR") -> str:
    """
    Format amount as currency
    
    Args:
        amount: Numeric amount
        currency: Currency code (default: IDR)
        
    Returns:
        Formatted currency string
    """
    if currency == "IDR":
        # Format for Indonesian Rupiah
        if amount >= 1_000_000_000_000:  # Trillion
            return f"Rp {amount/1_000_000_000_000:.1f}T"
        elif amount >= 1_000_000_000:  # Billion
            return f"Rp {amount/1_000_000_000:.1f}B"
        elif amount >= 1_000_000:  # Million
            return f"Rp {amount/1_000_000:.1f}M"
        else:
            return f"Rp {amount:,.0f}"
    else:
        return f"{currency} {amount:,.2f}"

def format_percentage(value: float, decimal_places: int = 2) -> str:
    """Format value as percentage"""
    return f"{value:.{decimal_places}f}%"

def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """Calculate percentage change between two values"""
    if old_value == 0:
        return 0.0 if new_value == 0 else float('inf')
    return ((new_value - old_value) / old_value) * 100

def get_quarter_dates(year: int, quarter: int) -> Tuple[datetime, datetime]:
    """Get start and end dates for a quarter"""
    quarter_starts = {
        1: (1, 1),
        2: (4, 1),
        3: (7, 1),
        4: (10, 1)
    }
    
    start_month, start_day = quarter_starts[quarter]
    start_date = datetime(year, start_month, start_day)
    
    if quarter == 4:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, start_month + 3, 1) - timedelta(days=1)
    
    return start_date, end_date

def validate_car(car_value: float) -> Dict[str, Any]:
    """Validate Capital Adequacy Ratio"""
    status = "PASS" if car_value >= 8.0 else "FAIL"
    health = "STRONG" if car_value >= 15.0 else "ADEQUATE" if car_value >= 10.0 else "WEAK"
    
    return {
        "value": car_value,
        "status": status,
        "health": health,
        "regulatory_minimum": 8.0,
        "target_minimum": 12.0,
        "buffer": car_value - 8.0
    }

def validate_npf(npf_value: float) -> Dict[str, Any]:
    """Validate Non-Performing Financing ratio"""
    status = "PASS" if npf_value <= 5.0 else "FAIL"
    health = "GOOD" if npf_value <= 2.0 else "ACCEPTABLE" if npf_value <= 3.5 else "CONCERNING" if npf_value <= 5.0 else "CRITICAL"
    
    return {
        "value": npf_value,
        "status": status,
        "health": health,
        "regulatory_maximum": 5.0,
        "target_maximum": 3.0,
        "excess": max(0, npf_value - 3.0)
    }

def calculate_composite_score(metrics: Dict[str, float], weights: Dict[str, float]) -> float:
    """
    Calculate weighted composite score
    
    Args:
        metrics: Dictionary of metric values
        weights: Dictionary of metric weights (must sum to 1.0)
        
    Returns:
        Composite score (0-100)
    """
    if abs(sum(weights.values()) - 1.0) > 0.001:
        raise ValueError("Weights must sum to 1.0")
    
    total_score = 0.0
    for metric, value in metrics.items():
        if metric in weights:
            total_score += value * weights[metric]
    
    return total_score

def categorize_risk_level(score: float) -> str:
    """Categorize risk level based on score"""
    if score >= 80:
        return "CRITICAL"
    elif score >= 60:
        return "HIGH"
    elif score >= 40:
        return "MEDIUM"
    elif score >= 20:
        return "LOW"
    else:
        return "VERY LOW"

def clean_text(text: str) -> str:
    """Clean text for processing"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep important punctuation
    text = re.sub(r'[^\w\s\.\,\;\:\-\%]', '', text)
    return text.strip()

def extract_numbers_from_text(text: str) -> List[float]:
    """Extract numerical values from text"""
    # Pattern to match numbers including decimals and percentages
    pattern = r'[-+]?\d*\.?\d+%?'
    matches = re.findall(pattern, text)
    
    numbers = []
    for match in matches:
        try:
            if match.endswith('%'):
                numbers.append(float(match[:-1]))
            else:
                numbers.append(float(match))
        except ValueError:
            continue
    
    return numbers

@lru_cache(maxsize=128)
def calculate_hash(content: str) -> str:
    """Calculate SHA256 hash of content"""
    return hashlib.sha256(content.encode()).hexdigest()

def retry_on_exception(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """Decorator to retry function on exception"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            current_delay = delay
            
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries >= max_retries:
                        raise
                    
                    time.sleep(current_delay)
                    current_delay *= backoff
                    
            return None
        return wrapper
    return decorator

def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split list into chunks"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
    """Flatten nested dictionary"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safe division with default value for division by zero"""
    if denominator == 0:
        return default
    return numerator / denominator

def get_trend_direction(values: List[float], threshold: float = 0.05) -> str:
    """
    Determine trend direction from a list of values
    
    Args:
        values: List of numerical values
        threshold: Minimum change to consider as trend
        
    Returns:
        'INCREASING', 'DECREASING', or 'STABLE'
    """
    if len(values) < 2:
        return 'STABLE'
    
    # Calculate average change
    changes = [values[i] - values[i-1] for i in range(1, len(values))]
    avg_change = np.mean(changes)
    
    # Normalize by the mean value
    mean_value = np.mean(values)
    if mean_value != 0:
        normalized_change = avg_change / mean_value
    else:
        normalized_change = 0
    
    if normalized_change > threshold:
        return 'INCREASING'
    elif normalized_change < -threshold:
        return 'DECREASING'
    else:
        return 'STABLE'

def create_summary_statistics(data: pd.DataFrame, columns: List[str]) -> Dict[str, Dict[str, float]]:
    """Create summary statistics for specified columns"""
    summary = {}
    
    for col in columns:
        if col in data.columns:
            summary[col] = {
                'mean': data[col].mean(),
                'median': data[col].median(),
                'std': data[col].std(),
                'min': data[col].min(),
                'max': data[col].max(),
                'q25': data[col].quantile(0.25),
                'q75': data[col].quantile(0.75)
            }
    
    return summary

def validate_date_range(start_date: datetime, end_date: datetime) -> bool:
    """Validate date range"""
    if start_date > end_date:
        return False
    if end_date > datetime.now():
        return False
    return True

def get_file_metadata(file_path: Path) -> Dict[str, Any]:
    """Get file metadata"""
    if not file_path.exists():
        return {}
    
    stats = file_path.stat()
    return {
        'size_bytes': stats.st_size,
        'size_mb': stats.st_size / (1024 * 1024),
        'created': datetime.fromtimestamp(stats.st_ctime),
        'modified': datetime.fromtimestamp(stats.st_mtime),
        'extension': file_path.suffix,
        'name': file_path.name
    }

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations"""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Limit length
    filename = filename[:255]
    return filename

def generate_report_filename(report_type: str, date: Optional[datetime] = None) -> str:
    """Generate standardized report filename"""
    if date is None:
        date = datetime.now()
    
    date_str = date.strftime('%Y%m%d_%H%M%S')
    safe_type = sanitize_filename(report_type.lower().replace(' ', '_'))
    
    return f"muamalat_{safe_type}_{date_str}.pdf"

# Color utilities for risk levels
RISK_COLORS = {
    'CRITICAL': '#dc3545',
    'HIGH': '#fd7e14',
    'MEDIUM': '#ffc107',
    'LOW': '#28a745',
    'VERY LOW': '#17a2b8'
}

def get_risk_color(risk_level: str) -> str:
    """Get color code for risk level"""
    return RISK_COLORS.get(risk_level.upper(), '#6c757d')

# Export all utilities
__all__ = [
    'format_currency',
    'format_percentage',
    'calculate_percentage_change',
    'get_quarter_dates',
    'validate_car',
    'validate_npf',
    'calculate_composite_score',
    'categorize_risk_level',
    'clean_text',
    'extract_numbers_from_text',
    'calculate_hash',
    'retry_on_exception',
    'chunk_list',
    'flatten_dict',
    'safe_divide',
    'get_trend_direction',
    'create_summary_statistics',
    'validate_date_range',
    'get_file_metadata',
    'sanitize_filename',
    'generate_report_filename',
    'get_risk_color',
    'RISK_COLORS'
]