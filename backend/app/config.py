import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Polygon.io API configuration
POLYGON_API_KEY = "QPuxCIPYpf7ukpeZb6SX8FpC61ms0GhZ"  # Using exact key from screenshot
POLYGON_BASE_URL = "https://api.polygon.io"

# List of assets to track
TRACKED_ASSETS = ["SPY", "QQQ", "AAPL", "TSLA", "NVDA", "VIX"]
