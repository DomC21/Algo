import asyncio
import logging
from datetime import datetime, timedelta
from app.data_providers.polygon_client import PolygonClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_connection():
    """Test the Polygon.io API connection by fetching SPY options chain."""
    try:
        async with PolygonClient() as client:
            # Test fetching option chain for SPY
            logger.info("Testing connection to Polygon.io API...")
            # Print the full URL and parameters for debugging
            test_url = f"{client.base_url}/v3/snapshot/options/SPY"
            logger.info(f"Making request to: {test_url}")
            logger.info(f"Using API key: {client.api_key}")
            
            data = await client._make_request("/v3/snapshot/options/SPY")
            logger.info("Successfully connected to Polygon.io API")
            logger.info(f"Response data: {str(data)[:200]}...")
                
    except Exception as e:
        logger.error(f"Error testing Polygon.io connection: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(test_connection())
