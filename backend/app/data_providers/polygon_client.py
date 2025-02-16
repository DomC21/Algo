import aiohttp
import asyncio
from datetime import datetime, timedelta
from typing import List, Optional, Dict
import logging

from app.models.option_data import OptionData, OptionType
from app.config import POLYGON_API_KEY, POLYGON_BASE_URL, TRACKED_ASSETS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PolygonAPIError(Exception):
    """Custom exception for Polygon API errors."""
    pass

class PolygonClient:
    """Client for interacting with the Polygon.io API for options data."""
    
    def __init__(self, api_key: str = POLYGON_API_KEY):
        self.api_key = api_key
        self.base_url = POLYGON_BASE_URL
        self.tracked_symbols = TRACKED_ASSETS
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make an HTTP request to the Polygon API."""
        if not self.session:
            raise RuntimeError("Client not initialized. Use 'async with' context manager.")
            
        # Build the full URL
        url = f"{self.base_url}{endpoint}"
        
        # Add API key as query parameter
        request_params = dict(params or {})
        request_params['apiKey'] = self.api_key  # Use exact key and parameter name from docs
        
        # Log request details for debugging
        logger.debug(f"Making request to: {url}")
        logger.debug(f"With params: {request_params}")
        
        # Set basic headers
        headers = {
            'Accept': 'application/json'
        }
        
        # Log full request details for debugging
        full_url = f"{url}?{'&'.join(f'{k}={v}' for k, v in request_params.items())}"
        logger.debug(f"Full request URL: {full_url}")
        
        # Add rate limiting delay
        await asyncio.sleep(0.2)  # Max 5 requests per second
        
        # Log the full request details for debugging
        full_url = f"{url}?{'&'.join(f'{k}={v}' for k, v in request_params.items())}"
        logger.debug(f"Making request to: {full_url}")
        logger.debug(f"Headers: {dict(self.session._default_headers)}")  # Log headers
        logger.debug(f"API Key used: {self.api_key.strip()}")
        
        try:
            async with self.session.get(url, params=request_params, headers=headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise PolygonAPIError(f"API request failed: {error_text}")
                
                data = await response.json()
                if data.get('status') == 'ERROR':
                    raise PolygonAPIError(f"API returned error: {data.get('error')}")
                    
                return data
        except aiohttp.ClientError as e:
            raise PolygonAPIError(f"Request failed: {str(e)}")
    
    async def get_option_chain(self, underlying_symbol: str, expiration_date: Optional[datetime] = None) -> List[OptionData]:
        """
        Fetch the full option chain for a given underlying symbol.
        If expiration_date is provided, only fetch options expiring on that date.
        """
        endpoint = "/v3/reference/options/contracts"
        params = {
            "underlying_ticker": underlying_symbol,
            "limit": 1000,
            "sort": "expiration_date",
            "order": "asc",
            "expired": "false"
        }
        
        if expiration_date:
            params["expiration_date"] = expiration_date.strftime("%Y-%m-%d")
        
        data = await self._make_request(endpoint, params)
        options_data = []
        
        for result in data.get('results', []):
            try:
                option = OptionData(
                    ticker=result['ticker'],
                    underlying_symbol=result['underlying_ticker'],
                    expiration_date=datetime.strptime(result['expiration_date'], "%Y-%m-%d"),
                    strike_price=float(result['strike_price']),
                    option_type=OptionType.CALL if result['type'] == 'call' else OptionType.PUT,
                    last_price=0.0,  # Will be updated with real-time data
                    bid_price=0.0,
                    ask_price=0.0,
                    bid_size=0,
                    ask_size=0,
                    volume=0,
                    open_interest=0
                )
                options_data.append(option)
            except (KeyError, ValueError) as e:
                logger.warning(f"Error parsing option data: {e}")
                continue
                
        return options_data
    
    async def get_option_quotes(self, option_symbol: str) -> OptionData:
        """Fetch real-time quotes for a specific option contract."""
        endpoint = f"/v2/last/trade/{option_symbol}"
        data = await self._make_request(endpoint)
        
        if not data.get('results'):
            raise PolygonAPIError(f"No quote data found for {option_symbol}")
            
        result = data['results']
        return OptionData(
            ticker=option_symbol,
            underlying_symbol=option_symbol.split("O:")[1][:4],
            expiration_date=datetime.now(),  # This needs to be parsed from the option symbol
            strike_price=0.0,  # This needs to be parsed from the option symbol
            option_type=OptionType.CALL,  # This needs to be parsed from the option symbol
            last_price=float(result['p']),
            bid_price=float(result.get('b', 0)),
            ask_price=float(result.get('a', 0)),
            bid_size=int(result.get('bs', 0)),
            ask_size=int(result.get('as', 0)),
            volume=int(result.get('v', 0)),
            open_interest=int(result.get('oi', 0))
        )
    
    async def get_historical_data(
        self, 
        option_symbol: str, 
        from_date: datetime, 
        to_date: datetime
    ) -> List[OptionData]:
        """Fetch historical data for a specific option contract."""
        endpoint = f"/v2/aggs/ticker/{option_symbol}/range/1/day/{from_date.strftime('%Y-%m-%d')}/{to_date.strftime('%Y-%m-%d')}"
        data = await self._make_request(endpoint)
        
        historical_data = []
        for result in data.get('results', []):
            try:
                option = OptionData(
                    ticker=option_symbol,
                    underlying_symbol=option_symbol.split("O:")[1][:4],
                    expiration_date=datetime.now(),  # This needs to be parsed from the option symbol
                    strike_price=0.0,  # This needs to be parsed from the option symbol
                    option_type=OptionType.CALL,  # This needs to be parsed from the option symbol
                    last_price=float(result['c']),
                    bid_price=0.0,
                    ask_price=0.0,
                    bid_size=0,
                    ask_size=0,
                    volume=int(result['v']),
                    open_interest=0,
                    timestamp=datetime.fromtimestamp(result['t'] / 1000.0)
                )
                historical_data.append(option)
            except (KeyError, ValueError) as e:
                logger.warning(f"Error parsing historical data: {e}")
                continue
                
        return historical_data
    
    def _calculate_greeks(self, data: dict) -> dict:
        """Calculate option Greeks if not provided by the API."""
        # TODO: Implement Black-Scholes model for Greeks calculations
        return {
            'delta': None,
            'gamma': None,
            'theta': None,
            'vega': None,
            'rho': None
        }
