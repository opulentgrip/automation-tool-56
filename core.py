import asyncio
from dataclasses import dataclass
from typing import Annotated, AsyncGenerator, Dict, List, Tuple

Price = Annotated[float, "Positive price in USDT"]
Volume = Annotated[float, "Volume in base asset"]


@dataclass(frozen=True)
class OrderTick:
    """Immutable representation of a crypto exchange orderbook tick."""

    symbol: str
    bid: Price
    ask: Price
    bid_vol: Volume
    ask_vol: Volume

    @property
    def spread_percentage(self) -> float:
        """Calculates bid-ask spread percentage relative to ask price."""
        return (self.ask - self.bid) / self.ask * 100.0


class ReactiveTickEngine:
    """Asynchronous stream processor for evaluating market tick dynamics."""

    def __init__(self, stream: AsyncGenerator[OrderTick, None]) -> None:
        self._stream = stream

    async def filter_tight_spreads(
        self, max_spread: float
    ) -> AsyncGenerator[OrderTick, None]:
        """Filters order ticks keeping only those under specified spread limit."""
        async for tick in self._stream:
            if tick.spread_percentage <= max_spread:
                yield tick

    async def compute_volume_imbalance(
        self, threshold: float = 0.2
    ) -> AsyncGenerator[Tuple[str, float], None]:
        """Extracts trading pair and normalized orderbook bid/ask volume imbalance."""
        async for tick in self._stream:
            total_vol = tick.bid_vol + tick.ask_vol
            if total_vol > 0:
                imbalance = (tick.bid_vol - tick.ask_vol) / total_vol
                if abs(imbalance) >= threshold:
                    yield tick.symbol, round(imbalance, 4)


async def simulate_market_feed(pairs: List[str]) -> AsyncGenerator[OrderTick, None]:
    """Synthesizes real-time market depth data for algorithmic evaluation."""
    import random

    for _ in range(10):
        for pair in pairs:
            base_price = random.uniform(0.5, 65000.0)
            spread = random.uniform(0.005, 0.5)
            yield OrderTick(
                symbol=pair,
                bid=base_price,
                ask=base_price * (1 + spread / 100),
                bid_vol=random.uniform(100.0, 50000.0),
                ask_vol=random.uniform(100.0, 50000.0),
            )
            await asyncio.sleep(0.001)
