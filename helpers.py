import math
from decimal import Decimal, InvalidOperation
from typing import Any, Callable, Optional

def safe_satoshi_convert(val: Any, default: int = 0) -> int:
    """Converts arbitrary ticker strings, floats, or sci-notation to Satoshis defensively."""
    if val is None or val == "":
        return default
    try:
        if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
            return default
        clean_str = str(val).replace(",", "").strip().split()[0]
        d = Decimal(clean_str)
        if d < 0:
            return default
        return int((d * Decimal("100000000")).to_integral_value())
    except (InvalidOperation, ValueError, IndexError, TypeError):
        return default

def mitigate_execution_faults(fallback_val: Optional[Any] = None):
    """Decorator to shield volatile exchange payload parsing from runtime arithmetic crashes."""
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
                if isinstance(res, float) and (math.isnan(res) or math.isinf(res)):
                    return fallback_val
                return res
            except (ZeroDivisionError, OverflowError, InvalidOperation, KeyError):
                return fallback_val
        return wrapper
    return decorator

@mitigate_execution_faults(fallback_val=0.0)
def calculate_impermanent_loss(price_ratio: float) -> float:
    """Calculates liquidity pool IL with automatic boundary edge-case handling."""
    if price_ratio <= 0:
        return 0.0
    sqrt_k = math.sqrt(price_ratio)
    il = (2 * sqrt_k / (1 + price_ratio)) - 1
    return round(abs(il), 8)