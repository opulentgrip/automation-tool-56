"""Asynchronous mempool signal processor for automated high-frequency crypto triggers."""

import asyncio
import math
from typing import AsyncIterator, Callable, Dict, List, Optional, Tuple, TypeAlias, Union

RawTxPayload: TypeAlias = Dict[str, Union[str, int, float]]
ProcessedSignal: TypeAlias = Tuple[str, float, float]
SignalFilter: TypeAlias = Callable[[RawTxPayload], bool]


class MempoolSignalHandler:
    """Processes raw mempool payload streams into actionable trading signals."""

    def __init__(
        self, min_gas_threshold: float = 20.0, liquidity_pool_address: Optional[str] = None
    ) -> None:
        """Initialize the mempool handler with custom gas and liquidity filters."""
        self.min_gas_threshold: float = min_gas_threshold
        self.target_pool: Optional[str] = liquidity_pool_address
        self._filters: List[SignalFilter] = [self._default_gas_filter]

    def _default_gas_filter(self, payload: RawTxPayload) -> bool:
        """Filter out transactions below the configured gas threshold."""
        gas_price: float = float(payload.get("gas_price", 0.0))
        return gas_price >= self.min_gas_threshold

    def register_filter(self, custom_filter: SignalFilter) -> None:
        """Attach a custom filtering callable to the pipeline evaluation chain."""
        self._filters.append(custom_filter)

    async def parse_tx_stream(
        self, stream: AsyncIterator[RawTxPayload]
    ) -> AsyncIterator[ProcessedSignal]:
        """Parse an incoming async stream of raw transaction dictionaries into signals."""
        async for tx in stream:
            if not all(f(tx) for f in self._filters):
                continue

            tx_hash: str = str(tx.get("hash", "0x00"))
            gas_gwei: float = float(tx.get("gas_price", 0.0))
            value_eth: float = float(tx.get("value", 0.0))

            slippage_est: float = round(math.log1p(value_eth) * 0.005, 4)
            yield (tx_hash, gas_gwei, slippage_est)


async def _self_test() -> None:
    """Run local module verification."""
    async def sample_stream() -> AsyncIterator[RawTxPayload]:
        txs: List[RawTxPayload] = [
            {"hash": "0xa1", "gas_price": 25.5, "value": 12.0},
            {"hash": "0xb2", "gas_price": 15.0, "value": 100.0},
            {"hash": "0xc3", "gas_price": 45.0, "value": 1.5},
        ]
        for tx in txs:
            await asyncio.sleep(0.001)
            yield tx

    handler = MempoolSignalHandler(min_gas_threshold=20.0)
    results: List[ProcessedSignal] = [sig async for sig in handler.parse_tx_stream(sample_stream())]
    assert len(results) == 2, f"Expected 2 signals, got {len(results)}"


if __name__ == "__main__":
    asyncio.run(_self_test())
