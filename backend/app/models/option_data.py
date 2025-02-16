from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

class OptionType(Enum):
    CALL = "CALL"
    PUT = "PUT"

@dataclass
class OptionData:
    # Core Option Data
    ticker: str  # Option symbol (e.g., "AAPL240419C150")
    underlying_symbol: str  # e.g., "AAPL"
    expiration_date: datetime
    strike_price: float
    option_type: OptionType
    
    # Market Data
    last_price: float
    bid_price: float
    ask_price: float
    bid_size: int
    ask_size: int
    volume: int
    open_interest: int
    
    # Greeks & Volatility Metrics
    delta: Optional[float] = None
    gamma: Optional[float] = None
    vega: Optional[float] = None
    theta: Optional[float] = None
    rho: Optional[float] = None
    implied_volatility: Optional[float] = None
    
    # Additional Data
    historical_volatility: Optional[float] = None
    intrinsic_value: Optional[float] = None
    extrinsic_value: Optional[float] = None
    moneyness: Optional[float] = None
    days_to_expiration: Optional[int] = None
    timestamp: datetime = None
