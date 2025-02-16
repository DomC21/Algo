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
            
            # Test with the simplest possible endpoint
            logger.info("Testing basic API connectivity...")
            # Test with the simplest possible endpoint
            test_endpoint = "/v2/aggs/ticker/AAPL/prev"  # Previous day's aggregates
            logger.debug(f"Full URL will be: {client.base_url}{test_endpoint}?apikey=IYH_RG0tjnQSvW7oNTRWdASXM6msKS7c")
            logger.debug(f"Using API key: {client.api_key}")
            logger.debug(f"Base URL: {client.base_url}")
            logger.info(f"Testing endpoint: {test_endpoint}")
            test_response = await client._make_request(test_endpoint)
            logger.debug(f"Full response: {test_response}")
            
            if test_response.get('status') == 'OK':
                logger.info("Successfully connected to Polygon.io API")
                
                # Now test the options endpoint
                options_endpoint = "/v3/reference/options/contracts"
                options_params = {
                    "underlying_ticker": "SPY",
                    "limit": 1,
                    "expired": "false"
                }
                logger.info(f"Testing options endpoint: {options_endpoint}")
                options_response = await client._make_request(options_endpoint, options_params)
                logger.debug(f"Options response: {options_response}")
            
            # Log response details for debugging
            if isinstance(test_response, dict):
                logger.debug(f"Response keys: {test_response.keys()}")
                if 'status' in test_response:
                    logger.debug(f"Response status: {test_response['status']}")
                if 'error' in test_response:
                    logger.debug(f"Response error: {test_response['error']}")
            
            if test_response.get('status') == 'OK':
                logger.info("Basic API connectivity successful")
                
                # Now test the options chain endpoint
                logger.info("Fetching SPY options chain...")
                options = await client.get_option_chain("SPY")
                
                if options:
                    logger.info(f"Successfully fetched {len(options)} SPY options")
                    sample_option = options[0]
                    logger.info(f"Sample option: {sample_option}")
                else:
                    logger.info("No options data returned")
            else:
                logger.error("Failed basic API connectivity test")
                
    except Exception as e:
        logger.error(f"Error testing Polygon.io connection: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(test_connection())
