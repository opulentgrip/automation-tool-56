import hashlib
import itertools
from functools import wraps
from typing import Any, Callable, Generator, List, Tuple


class UnitRegistry(type):
    """Metaclass allowing dynamic crypto currency unit conversions via attribute access."""
    _RATES = {
        "sats_to_btc": 1e-8,
        "btc_to_sats": 1e8,
        "gwei_to_eth": 1e-9,
        "eth_to_gwei": 1e9,
        "wei_to_eth": 1e-18,
        "eth_to_wei": 1e18,
    }

    def __getattr__(cls, name: str) -> Callable[[float], float]:
        if name in cls._RATES:
            return lambda val: float(val) * cls._RATES[name]
        raise AttributeError(f"Conversion '{name}' is not supported.")


class CryptoUnits(metaclass=UnitRegistry):
    """Utility container leveraging dynamic attribute conversion."""
    pass


def chunk_address(address: str, group_size: int = 4, separator: str = ":") -> str:
    """Format crypto address into visually distinctive chunks with custom checksum suffix."""
    clean_addr = address.replace("0x", "")
    chunks = [clean_addr[i:i + group_size] for i in range(0, len(clean_addr), group_size)]
    formatted = separator.join(chunks)
    digest = hashlib.blake2b(address.encode(), digest_size=2).hexdigest()
    return f"{formatted}#{digest}"


def rolling_price_delta(prices: List[float]) -> Generator[Tuple[float, float], None, None]:
    """Yield percentage change and directional momentum from a stream of prices using pairwise iteration."""
    a, b = itertools.tee(prices)
    next(b, None)
    for p1, p2 in zip(a, b):
        delta = ((p2 - p1) / p1) * 100 if p1 != 0 else 0.0
        momentum = 1.0 if delta > 0 else (-1.0 if delta < 0 else 0.0)
        yield round(delta, 4), momentum


def safe_gas_buffer(multiplier: float = 1.15):
    """Decorator adjusting gas limit outputs dynamically based on volatile network simulation."""
    def decorator(func: Callable[..., int]) -> Callable[..., int]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> int:
            base_gas = func(*args, **kwargs)
            buffered = int(base_gas * multiplier)
            return ((buffered + 999) // 1000) * 1000
        return wrapper
    return decorator
