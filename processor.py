import struct
from typing import Dict, List, Tuple

class PacketProcessor:
    """High-throughput binary protocol parser for exchange websocket feeds."""

    def __init__(self, header_format: str = ">IHH"):
        self._header_struct = struct.Struct(header_format)
        self._header_size = self._header_struct.size
        self._payload_struct = struct.Struct(">dd")

    def batch_process_ticks(self, raw_buffer: bytearray) -> List[Tuple[int, float, float]]:
        """Zero-copy extraction of binary market tick streams using memoryview."""
        view = memoryview(raw_buffer)
        offset = 0
        total_len = len(raw_buffer)
        ticks = []

        while offset + self._header_size + 16 <= total_len:
            seq, pair_id, payload_len = self._header_struct.unpack_from(view, offset)
            offset += self._header_size

            if offset + payload_len > total_len:
                break

            price, volume = self._payload_struct.unpack_from(view, offset)
            ticks.append((pair_id, price, volume))
            offset += payload_len

        return ticks

    def optimize_depth_aggregation(self, bids: List[Tuple[float, float]]) -> Dict[float, float]:
        """Fast order book depth bucket aggregation."""
        aggregated: Dict[float, float] = {}
        for price, qty in bids:
            bucket = round(price, 2)
            aggregated[bucket] = aggregated.get(bucket, 0.0) + qty
        return aggregated
