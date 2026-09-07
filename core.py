import time
from collections import deque
from typing import Tuple, Optional

class FastTicker:
    __slots__ = ('limit', 'ticks', 'pv_sum', 'v_sum')
    
    def __init__(self, limit: int = 10000):
        self.limit = limit
        self.ticks = deque()
        self.pv_sum = 0.0
        self.v_sum = 0.0

    def add_tick(self, price: float, volume: float) -> None:
        if len(self.ticks) >= self.limit:
            old_p, old_v = self.ticks.popleft()
            self.pv_sum -= old_p * old_v
            self.v_sum -= old_v
        
        self.ticks.append((price, volume))
        self.pv_sum += price * volume
        self.v_sum += volume

    def get_vwap(self) -> float:
        return self.pv_sum / self.v_sum if self.v_sum > 0 else 0.0

    def clear(self) -> None:
        self.ticks.clear()
        self.pv_sum = 0.0
        self.v_sum = 0.0