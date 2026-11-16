import logging
from typing import Any, Dict, List
import functools

logger = logging.getLogger('automation-tool-56')

class DataSanitizer:
    """Static utility for crypto payload normalization."""
    @staticmethod
    def strip_keys(data: Dict[str, Any], sensitive_keys: List[str] = None) -> Dict[str, Any]:
        sensitive_keys = sensitive_keys or ['api_secret', 'private_key', 'mnemonic']
        return {k: ('***' if k in sensitive_keys else v) for k, v in data.items()}

def atomic_retry(attempts: int = 3):
    """Decorator for transient crypto exchange API failures."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    logger.warning(f"retry {i+1}/{attempts} due to {e}")
            raise last_ex
        return wrapper
    return decorator

def format_crypto_amount(val: float, precision: int = 8) -> str:
    """Force scientific notation avoidance for crypto precision."""
    return f"{val:.{precision}f}".rstrip('0').rstrip('.')

def batch_process(items: List[Any], chunk_size: int = 5):
    """Generator for chunking volatile crypto requests."""
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]