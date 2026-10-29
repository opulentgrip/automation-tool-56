import struct
from typing import Dict, Any

class FastTickAggregator:
    """High-throughput tick buffer with zero-allocation VWAP calculation."""
    __slots__ = ('_buffer', '_size', '_head', '_count', '_volume_sum', '_pv_sum')

    def __init__(self, capacity: int = 1000) -> None:
        self._size = capacity
        self._buffer = bytearray(capacity * 24)
        self._head = 0
        self._count = 0
        self._volume_sum = 0.0
        self._pv_sum = 0.0

    def push(self, price: float, volume: float, timestamp_ms: int) -> None:
        offset = self._head * 24
        if self._count == self._size:
            old_price, old_vol, _ = struct.unpack_from('<ddQ', self._buffer, offset)
            self._volume_sum -= old_vol
            self._pv_sum -= old_price * old_vol
        else:
            self._count += 1

        struct.pack_into('<ddQ', self._buffer, offset, price, volume, timestamp_ms)
        self._volume_sum += volume
        self._pv_sum += price * volume
        self._head = (self._head + 1) % self._size

    def calculate_vwap(self) -> float:
        if self._volume_sum == 0.0 or self._count == 0:
            return 0.0
        return self._pv_sum / self._volume_sum

    def get_batch_stats(self) -> Dict[str, float]:
        if self._count == 0:
            return {'vwap': 0.0, 'min': 0.0, 'max': 0.0, 'volume': 0.0}

        mv = memoryview(self._buffer)
        prices = []
        for i in range(self._count):
            idx = (self._head - self._count + i) % self._size
            p, _, _ = struct.unpack_from('<ddQ', mv, idx * 24)
            prices.append(p)

        return {
            'vwap': self.calculate_vwap(),
            'min': min(prices),
            'max': max(prices),
            'volume': self._volume_sum
        }

    def clear(self) -> None:
        self._head = 0
        self._count = 0
        self._volume_sum = 0.0
        self._pv_sum = 0.0
