import time
from typing import Dict, List, Union, Callable

CryptoAsset = Union[str, float]

def normalize_ticker(ticker: str) -> str:
    """Converts symbol to uppercase crypto standard."""
    return ticker.strip().upper()

def batch_process_wallets(addresses: List[str], task: Callable[[str], bool]) -> Dict[str, bool]:
    """Executes async-style task verification for wallet list."""
    results: Dict[str, bool] = {}
    for addr in addresses:
        try:
            results[addr] = task(addr)
        except Exception:
            results[addr] = False
    return results

def get_market_delta(price_now: CryptoAsset, price_prev: CryptoAsset) -> float:
    """Calculates percentage swing between two market snapshots."""
    p1, p2 = float(price_now), float(price_prev)
    if p2 == 0:
        return 0.0
    return ((p1 - p2) / p2) * 100

def retry_request(retries: int = 3, delay: float = 0.5) -> Callable:
    """Decorator for resilient crypto exchange api calls."""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            last_err = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_err = e
                    time.sleep(delay * (i + 1))
            raise last_err
        return wrapper
    return decorator