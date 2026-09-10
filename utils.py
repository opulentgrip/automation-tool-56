import time
import functools
import random
from typing import Callable, Any

class CryptoEdgeCaseError(Exception):
    """Base exception for crypto automation edge cases."""
    pass

class PrecisionLossError(CryptoEdgeCaseError):
    """Raised when float conversion risks precision loss in crypto amounts."""
    pass

def handle_crypto_edge_cases(max_retries: int = 3, min_precision: int = 8):
    """Decorator to handle network glitches and numeric precision edge cases."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            retries = 0
            while retries <= max_retries:
                try:
                    result = func(*args, **kwargs)
                    if isinstance(result, float) and result < 1e-6:
                        str_val = f"{result:.16f}"
                        decimals = len(str_val.split('.')[1].rstrip('0'))
                        if decimals < min_precision:
                            raise PrecisionLossError(f"Precision loss on value: {result}")
                    return result
                except (ConnectionError, TimeoutError) as err:
                    retries += 1
                    if retries > max_retries:
                        raise CryptoEdgeCaseError(f"Exceeded max retries: {err}") from err
                    time.sleep((2 ** retries) + random.uniform(0.1, 0.5))
                except PrecisionLossError:
                    return str(args[0]) if args else "0.0"
        return wrapper
    return decorator