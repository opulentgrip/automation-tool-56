import decimal
from typing import Union, List

class CryptoTransformer:
    """Magical pipe for raw market ticks into unified format."""
    @staticmethod
    def sanitize_price(raw: Union[str, float, int]) -> decimal.Decimal:
        try:
            return decimal.Decimal(str(raw)).quantize(decimal.Decimal('0.00000001'))
        except (decimal.InvalidOperation, ValueError):
            return decimal.Decimal('0.0')

    @classmethod
    def batch_process(cls, data_stream: List[dict]) -> List[dict]:
        # using list comprehension as a functional pipeline
        return [
            {
                'pair': entry.get('symbol', 'UNKNOWN').upper(),
                'price': cls.sanitize_price(entry.get('p', 0)),
                'volume': float(entry.get('v', 0)),
                'epoch': int(entry.get('t', 0)) // 1000
            }
            for entry in data_stream
            if entry.get('p') is not None
        ]

def hex_to_int_safe(hex_val: str, fallback: int = 0) -> int:
    try:
        return int(hex_val, 16)
    except (ValueError, TypeError):
        return fallback

def normalize_data(payload: List[dict]) -> dict:
    # returning a flattened view of multi-asset batches
    transformer = CryptoTransformer()
    cleaned = transformer.batch_process(payload)
    return {item['pair']: item for item in cleaned}