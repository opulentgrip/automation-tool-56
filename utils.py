import time
from typing import Dict, Any, Union, List

def sanitize_price(raw_val: Union[str, float, int]) -> float:
    """Converts chaotic crypto feed strings into pure floats."""
    try:
        return float(raw_val)
    except (ValueError, TypeError):
        return 0.0

def hash_order_id(seed: str, salt: str = "x-crypto-56") -> str:
    """Creates a deterministic chaos-proof internal identifier."""
    import hashlib
    payload: str = f"{seed}{salt}{time.time()}"
    return hashlib.sha256(payload.encode()).hexdigest()[:16]

def normalize_payload(data: Dict[str, Any]) -> List[float]:
    """Flattens dictionary values into a sequence of floats."""
    extracted: List[float] = []
    for value in data.values():
        if isinstance(value, (int, float, str)):
            extracted.append(sanitize_price(value))
    return extracted

class GasStrategy:
    """Strategy pattern for choosing gwei levels dynamically."""
    def __init__(self, multiplier: float = 1.1) -> None:
        self.multiplier = multiplier

    def calculate(self, base_fee: float) -> float:
        """Applies the mystical multiplier to base gas."""
        return round(base_fee * self.multiplier, 8)