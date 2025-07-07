"""
Logging configuration
"""

import logging
import sys
from datetime import datetime

def setup_logger(name: str = "TONY_M3TA_BOT", level: int = logging.INFO) -> logging.Logger:
    """Setup and configure logger"""
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger

def log_error(logger: logging.Logger, message: str, exc_info: bool = True):
    """Log error with exception info"""
    logger.error(message, exc_info=exc_info)

def log_api_call(logger: logging.Logger, endpoint: str, status_code: int, duration: float = None):
    """Log API call details"""
    message = f"API Call: {endpoint} - Status: {status_code}"
    if duration:
        message += f" - Duration: {duration:.2f}s"
    
    if status_code >= 400:
        logger.error(message)
    elif status_code >= 300:
        logger.warning(message)
    else:
        logger.info(message)
