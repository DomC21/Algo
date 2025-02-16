import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Polygon.io API configuration
POLYGON_API_KEY = "lYH_RG0tjnQSvW7oNTRWdASXM6msKS7c"
POLYGON_BASE_URL = "https://api.polygon.io"

# List of assets to track
TRACKED_ASSETS = ["SPY", "QQQ", "AAPL", "TSLA", "NVDA", "VIX"]
