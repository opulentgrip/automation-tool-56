import time
from typing import Dict, List, Optional


class TickerBuffer:
    __slots__ = ("_size", "_buffer", "_index", "_sum_price", "_sum_vol")

    def __init__(self, size: int = 1000):
        self._size = size
        self._buffer: List[Optional[tuple]] = [None] * size
        self._index = 0
        self._sum_price = 0.0
        self._sum_vol = 0.0

    def push(self, price: float, volume: float) -> None:
        old = self._buffer[self._index]
        if old is not None:
            self._sum_price -= old[0]
            self._sum_vol -= old[1]

        self._buffer[self._index] = (price, volume)
        self._sum_price += price
        self._sum_vol += volume
        self._index = (self._index + 1) % self._size

    def volume_weighted_average_price(self) -> float:
        if self._sum_vol == 0.0:
            return 0.0
        return self._sum_price / self._sum_vol


class CoreEngine:
    def __init__(self, pairs: List[str]):
        self.buffers: Dict[str, TickerBuffer] = {
            pair: TickerBuffer() for pair in pairs
        }

    def process_feed(self, ticks: List[tuple]) -> Dict[str, float]:
        for pair, price, vol in ticks:
            if pair in self.buffers:
                self.buffers[pair].push(price, vol)
        return {
            pair: buf.volume_weighted_average_price()
            for pair, buf in self.buffers.items()
        }
