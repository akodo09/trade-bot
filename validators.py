import re
from typing import Tuple, Optional

def validate_symbol(symbol: str) -> bool:
    return bool(re.match(r"^[A-Z0-9]{3,20}$", symbol.upper()))

def validate_side(side: str) -> bool:
    return side.upper() in ["BUY", "SELL"]

def validate_order_type(order_type: str) -> bool:
    return order_type.upper() in ["MARKET", "LIMIT"]

def validate_quantity(qty: str) -> Tuple[bool, Optional[float]]:
    try:
        val = float(qty)
        if val > 0:
            return True, val
        return False, None
    except ValueError:
        return False, None

def validate_price(price: str, order_type: str) -> Tuple[bool, Optional[float]]:
    if order_type.upper() == "MARKET":
        return True, 0.0
    try:
        val = float(price)
        if val > 0:
            return True, val
        return False, None
    except ValueError:
        return False, None
