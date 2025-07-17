"""
Logging utilities for Bank Muamalat Health Monitoring System
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

def setup_logger(
    name: str,
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Set up a logger with both file and console handlers
    
    Args:
        name: Logger name
        level: Logging level
        log_file: Optional log file path
        format_string: Optional custom format string
    
    Returns:
        Configured logger instance
    """
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Default format
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    formatter = logging.Formatter(format_string)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        # Create logs directory if it doesn't exist
        log_dir = Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        # Default log file
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        today = datetime.now().strftime("%Y%m%d")
        default_log_file = logs_dir / f"app_{today}.log"
        
        file_handler = logging.FileHandler(default_log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """
    Get an existing logger or create a new one
    
    Args:
        name: Logger name
    
    Returns:
        Logger instance
    """
    return logging.getLogger(name)

class StreamlitLogHandler(logging.Handler):
    """Custom log handler for Streamlit"""
    
    def emit(self, record):
        """Emit log record to Streamlit"""
        try:
            import streamlit as st
            msg = self.format(record)
            
            if record.levelno >= logging.ERROR:
                st.error(msg)
            elif record.levelno >= logging.WARNING:
                st.warning(msg)
            elif record.levelno >= logging.INFO:
                st.info(msg)
            else:
                st.text(msg)
        except Exception:
            # Fallback to standard logging if Streamlit is not available
            print(f"LOG: {self.format(record)}")

def setup_streamlit_logger(name: str) -> logging.Logger:
    """
    Set up a logger that displays messages in Streamlit
    
    Args:
        name: Logger name
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Avoid adding handlers multiple times
    if any(isinstance(h, StreamlitLogHandler) for h in logger.handlers):
        return logger
    
    # Add Streamlit handler
    streamlit_handler = StreamlitLogHandler()
    streamlit_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    streamlit_handler.setFormatter(formatter)
    logger.addHandler(streamlit_handler)
    
    return logger

# Pre-configured loggers
main_logger = setup_logger("bank_muamalat_monitor")
data_logger = setup_logger("data_processor")
ai_logger = setup_logger("ai_orchestrator")

# Export
__all__ = [
    'setup_logger',
    'get_logger',
    'setup_streamlit_logger',
    'StreamlitLogHandler',
    'main_logger',
    'data_logger',
    'ai_logger'
]