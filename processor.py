import struct
from typing import Generator, Dict, Union

class FastCryptoProcessor:
    """
    Optimized parser for raw binary transaction streams using memoryview
    to avoid object allocation overhead during high-throughput ingestion.
    """
    # Layout: 20 bytes (to) + 20 bytes (from) + 8 bytes (value uint64) + 4 bytes (nonce uint32)
    TX_STRUCT_FORMAT = ">20s20sQI"
    TX_SIZE = struct.calcsize(TX_STRUCT_FORMAT)

    def __init__(self, raw_buffer: bytes):
        self.buffer = memoryview(raw_buffer)

    def fast_parse(self) -> Generator[Dict[str, Union[str, int]], None, None]:
        """
        Extracts transaction details efficiently using memoryview slicing.
        """
        buffer_len = len(self.buffer)
        offset = 0
        tx_size = self.TX_SIZE
        unpack = struct.unpack_from

        while offset + tx_size <= buffer_len:
            to_addr_bytes, from_addr_bytes, value, nonce = unpack(
                self.TX_STRUCT_FORMAT, self.buffer, offset
            )
            yield {
                "to": f"0x{to_addr_bytes.hex()}",
                "from": f"0x{from_addr_bytes.hex()}",
                "value_gwei": value,
                "nonce": nonce
            }
            offset += tx_size

    @classmethod
    def aggregate_volume(cls, raw_buffer: bytes) -> int:
        """
        Ultra-fast volume extraction bypassing dict creation entirely.
        """
        view = memoryview(raw_buffer)
        total_volume = 0
        tx_size = cls.TX_SIZE
        value_offset = 40
        
        for offset in range(0, len(view) - tx_size + 1, tx_size):
            val_bytes = view[offset + value_offset : offset + value_offset + 8]
            total_volume += int.from_bytes(val_bytes, byteorder="big")
            
        return total_volume