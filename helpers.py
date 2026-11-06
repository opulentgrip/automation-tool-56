import math
from typing import Any, Callable, Tuple, Union


class ValueChain:
    """Fluent pipe wrapper for data transformations on crypto metrics."""

    def __init__(self, value: Any):
        self.value = value

    def __or__(self, func: Callable[[Any], Any]) -> "ValueChain":
        return ValueChain(func(self.value))

    def unwrap(self) -> Any:
        return self.value


def to_base_unit(amount: Union[int, float, str], decimals: int = 18) -> float:
    """Converts raw crypto units (wei/sats) to float base currency."""
    return float(amount) / (10**decimals)


def mask_address(address: str, head: int = 6, tail: int = 4) -> str:
    """Truncates public key addresses for UI display with ellipsis."""
    if not address or len(address) <= head + tail:
        return address
    return f"{address[:head]}...{address[-tail:]}"


def format_compact_val(value: float, precision: int = 2) -> str:
    """Formats large financial values with dynamic metric suffixes."""
    if value == 0:
        return "0.00"
    suffixes = ["", "K", "M", "B", "T"]
    magnitude = max(
        0, min(len(suffixes) - 1, int(math.floor(math.log10(abs(value)) / 3)))
    )
    scaled = value / (10 ** (magnitude * 3))
    return f"{scaled:.{precision}f}{suffixes[magnitude]}"


def calculate_price_delta(
    old_price: float, new_price: float
) -> Tuple[float, str]:
    """Calculates percentage price change and market directional bias."""
    if old_price == 0:
        return 0.0, "NEUTRAL"
    pct_change = ((new_price - old_price) / old_price) * 100
    direction = (
        "BULL" if pct_change > 0 else ("BEAR" if pct_change < 0 else "NEUTRAL")
    )
    return round(pct_change, 4), direction
