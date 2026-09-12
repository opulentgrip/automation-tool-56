import math
from collections import deque
from typing import Dict, Generator, List, Tuple


class DynamicVWAPAggregator:
    """Sliding-window VWAP calculator using custom decay weighting."""

    def __init__(self, window_size: int = 50, decay: float = 0.99):
        self.window_size = window_size
        self.decay = decay
        self._buffers: Dict[str, deque] = {}

    def process_stream(
        self, ticks: List[Tuple[str, float, float, float]]
    ) -> Generator[Dict[str, float], None, None]:
        for sym, price, vol, ts in ticks:
            if sym not in self._buffers:
                self._buffers[sym] = deque(maxlen=self.window_size)

            self._buffers[sym].append((price, vol, ts))

            weighted_vol_sum = 0.0
            weighted_pv_sum = 0.0
            buf = self._buffers[sym]

            for idx, (p, v, _) in enumerate(reversed(buf)):
                weight = math.pow(self.decay, idx)
                weighted_vol_sum += v * weight
                weighted_pv_sum += p * v * weight

            vwap = (
                weighted_pv_sum / weighted_vol_sum
                if weighted_vol_sum > 0
                else price
            )
            yield {
                "symbol": sym,
                "vwap": round(vwap, 8),
                "depth": len(buf),
                "latest_price": price,
            }


def parse_crypto_ticks(raw_data: List[Dict]) -> List[Tuple[str, float, float, float]]:
    """Parses heterogeneous websocket payloads into standardized tuples."""
    ticks = []
    for item in raw_data:
        sym = str(item.get("s") or item.get("symbol") or "BTCUSDT").upper()
        price = float(item.get("p") or item.get("price") or 0.0)
        vol = float(item.get("q") or item.get("v") or item.get("volume") or 0.0)
        ts = float(item.get("T") or item.get("t") or item.get("timestamp") or 0.0)
        if price > 0 and vol > 0:
            ticks.append((sym, price, vol, ts))
    return ticks
