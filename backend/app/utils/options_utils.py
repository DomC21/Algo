from datetime import datetime
from typing import Optional

def calculate_days_to_expiration(expiration_date: datetime) -> int:
    """Calculate the number of days until option expiration."""
    return (expiration_date - datetime.now()).days

def calculate_moneyness(underlying_price: float, strike_price: float, option_type: str) -> float:
    """Calculate the moneyness ratio of an option."""
    return underlying_price / strike_price

def calculate_intrinsic_value(underlying_price: float, strike_price: float, option_type: str) -> float:
    """Calculate the intrinsic value of an option."""
    if option_type == "CALL":
        return max(0, underlying_price - strike_price)
    else:  # PUT
        return max(0, strike_price - underlying_price)

def calculate_historical_volatility(prices: list[float], window: int = 30) -> Optional[float]:
    """Calculate historical volatility from a list of prices."""
    # TODO: Implement historical volatility calculation
    pass
