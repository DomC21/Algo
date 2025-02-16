import asyncio
import logging
from datetime import datetime, timedelta
from app.data_providers.polygon_client import PolygonClient

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def test_connection():
    """Test the Polygon.io API connection by fetching SPY options chain."""
    try:
        async with PolygonClient() as client:
            logger.info("Testing connection to Polygon.io API...")
            logger.info("Fetching SPY options chain...")
            
            # Test the options chain endpoint
            options = await client.get_option_chain("SPY")
            
            if options:
                logger.info(f"Successfully fetched {len(options)} SPY options")
                sample_option = options[0]
                logger.info(f"Sample option: {sample_option}")
            else:
                logger.info("No options data returned")
                
    except Exception as e:
        logger.error(f"Error testing Polygon.io connection: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(test_connection())
