import math
import struct


class FastOrderBookStream:
    """Pre-allocated circular ring buffer using bytearray for zero-allocation tick aggregation."""

    __slots__ = ("_buffer", "_capacity", "_head", "_count", "_fmt", "_item_size")

    def __init__(self, capacity: int = 1000):
        self._fmt = "<ddd"  # timestamp, price, volume (24 bytes per tick)
        self._item_size = struct.calcsize(self._fmt)
        self._capacity = capacity
        self._buffer = bytearray(self._item_size * capacity)
        self._head = 0
        self._count = 0

    def push_tick(self, timestamp: float, price: float, volume: float) -> None:
        """Pushes a tick directly into pre-allocated memory offset."""
        offset = self._head * self._item_size
        struct.pack_into(self._fmt, self._buffer, offset, timestamp, price, volume)
        self._head = (self._head + 1) % self._capacity
        if self._count < self._capacity:
            self._count += 1

    def compute_vwap(self) -> float:
        """Calculates Volume-Weighted Average Price using memoryview slicing."""
        if self._count == 0:
            return 0.0

        total_pv = 0.0
        total_volume = 0.0
        size = self._item_size
        view = memoryview(self._buffer)

        for i in range(self._count):
            idx = ((self._head - 1 - i) + self._capacity) % self._capacity
            offset = idx * size
            _, price, volume = struct.unpack_from(self._fmt, view, offset)
            total_pv += price * volume
            total_volume += volume

        return total_pv / total_volume if total_volume > 0 else 0.0

    def calculate_volatility(self) -> float:
        """Log-return volatility calculation over buffered prices."""
        if self._count < 2:
            return 0.0

        size = self._item_size
        view = memoryview(self._buffer)
        prices = []

        for i in range(self._count):
            idx = (self._head - self._count + i) % self._capacity
            offset = idx * size
            _, price, _ = struct.unpack_from(self._fmt, view, offset)
            prices.append(price)

        log_returns = [
            math.log(prices[i] / prices[i - 1]) for i in range(1, len(prices))
        ]
        mean_return = sum(log_returns) / len(log_returns)
        variance = sum((r - mean_return) ** 2 for r in log_returns) / len(
            log_returns
        )
        return math.sqrt(variance)
