from decimal import Decimal, ROUND_DOWN
import random
from typing import Tuple, Union, List, Generator, Any


class UnitConverter:
    """High-precision crypto currency unit conversion engine."""
    
    RATES = {
        'wei': Decimal('1'),
        'gwei': Decimal('10') ** 9,
        'ether': Decimal('10') ** 18,
        'satoshi': Decimal('1'),
        'btc': Decimal('10') ** 8,
    }

    @classmethod
    def convert(cls, value: Union[int, float, str], from_unit: str, to_unit: str) -> Decimal:
        amount = Decimal(str(value))
        source = cls.RATES[from_unit.lower()]
        target = cls.RATES[to_unit.lower()]
        converted = (amount * source) / target
        return converted.quantize(Decimal('0.00000001'), rounding=ROUND_DOWN)


def mask_address(address: str, prefix_len: int = 6, suffix_len: int = 4) -> str:
    """Truncates long blockchain wallet addresses for clean display output."""
    if not address or len(address) <= (prefix_len + suffix_len + 3):
        return address
    return f"{address[:prefix_len]}...{address[-suffix_len:]}"


def calculate_slippage(price: Union[float, Decimal], slippage_pct: float) -> Tuple[Decimal, Decimal]:
    """Returns minimum and maximum price thresholds based on acceptable slippage percentage."""
    base = Decimal(str(price))
    delta = base * (Decimal(str(slippage_pct)) / Decimal('100'))
    return base - delta, base + delta


def jitter_backoff(attempt: int, base_delay: float = 0.5, max_delay: float = 30.0) -> float:
    """Calculates exponential backoff delay with random jitter for RPC rate limiting."""
    factor = min(max_delay, base_delay * (2 ** attempt))
    return random.uniform(0.5 * factor, factor)


def chunk_requests(items: List[Any], chunk_size: int) -> Generator[List[Any], None, None]:
    """Splits a payload list into chunks for batched RPC API requests."""
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]
