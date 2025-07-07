"""
Configuration settings
"""

import os
from typing import Optional

# Bot configuration
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "7709151940:AAFkQ2z8sgxwdlAhmGDk8G1lJ6KjKDZFBrw")

# API configuration
COINGECKO_BASE_URL: str = "https://api.coingecko.com/api/v3"
COINGECKO_API_KEY: Optional[str] = os.getenv("COINGECKO_API_KEY")  # Optional for free tier

# Monitoring configuration
PRICE_CHECK_INTERVAL: int = int(os.getenv("PRICE_CHECK_INTERVAL", "120"))  # seconds
PRICE_TOLERANCE: float = float(os.getenv("PRICE_TOLERANCE", "0.01"))  # 1%

# Rate limiting
MAX_REQUESTS_PER_MINUTE: int = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "50"))
MAX_WATCHES_PER_USER: int = int(os.getenv("MAX_WATCHES_PER_USER", "10"))

# Logging configuration
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

# Application settings
APP_NAME: str = "TONY_M3TA_BOT"
VERSION: str = "1.0.0"
DESCRIPTION: str = "Cryptocurrency Price Monitoring and Sniping Bot"

# Feature flags
ENABLE_DETAILED_LOGGING: bool = os.getenv("ENABLE_DETAILED_LOGGING", "False").lower() == "true"
ENABLE_PRICE_HISTORY: bool = os.getenv("ENABLE_PRICE_HISTORY", "False").lower() == "true"

# Validation
if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
    raise ValueError("BOT_TOKEN environment variable is required")

# Export commonly used settings
__all__ = [
    'BOT_TOKEN',
    'COINGECKO_BASE_URL',
    'PRICE_CHECK_INTERVAL',
    'PRICE_TOLERANCE',
    'MAX_REQUESTS_PER_MINUTE',
    'MAX_WATCHES_PER_USER',
    'LOG_LEVEL',
    'APP_NAME',
    'VERSION'
]
