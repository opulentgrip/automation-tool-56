import math
from typing import List, Dict, Tuple, Any

class OrderBookAggregator:
    """Creative depth aggregator using dynamic logarithmic price bucket normalization."""
    def __init__(self, step_percentage: float = 0.5):
        self.step_pct = max(0.01, min(step_percentage, 5.0)) / 100.0

    def _calculate_bucket(self, price: float) -> float:
        factor = 1.0 + self.step_pct
        bucket_idx = math.floor(math.log(price, factor))
        return round(math.pow(factor, bucket_idx), 4)

    def aggregate_depth(self, raw_orders: List[Tuple[float, float]]) -> Dict[float, float]:
        """Aggregates [(price, amount), ...] into price buckets using generator mapping."""
        buckets: Dict[float, float] = {}
        grouped = (
            (self._calculate_bucket(price), amount)
            for price, amount in sorted(raw_orders, key=lambda x: x[0])
        )
        for bucket_price, amount in grouped:
            buckets[bucket_price] = round(buckets.get(bucket_price, 0.0) + amount, 8)
        return dict(sorted(buckets.items()))

def decode_compact_ticker(raw_payload: str) -> Dict[str, Any]:
    """Unpacks custom base-36 encoded crypto ticker payload."""
    parts = raw_payload.strip().split(":")
    if len(parts) != 4:
        raise ValueError(f"Invalid compact ticker payload format: {raw_payload}")
    
    symbol, raw_price, raw_vol, raw_ts = parts
    price = int(raw_price, 36) / 10**4
    volume = int(raw_vol, 36) / 10**4
    
    return {
        "symbol": symbol.upper(),
        "price": float(price),
        "volume": float(volume),
        "timestamp": int(raw_ts)
    }
