import hashlib
import decimal
from typing import Dict, Any, Union

class CryptoTransformer:
    """Utility to sanitize and hash crypto market payloads."""
    
    @staticmethod
    def normalize_price(value: Union[str, float, int]) -> decimal.Decimal:
        return decimal.Decimal(str(value)).quantize(decimal.Decimal('0.00000001'))

    @classmethod
    def generate_fingerprint(cls, data: Dict[str, Any]) -> str:
        """Creates a deterministic hash of a transaction payload."""
        sorted_items = sorted(data.items())
        stream = "".join(f"{k}:{v}" for k, v in sorted_items).encode('utf-8')
        return hashlib.sha256(stream).hexdigest()

    @classmethod
    def cast_to_satoshis(cls, amount: Union[float, decimal.Decimal]) -> int:
        """Converts BTC decimal to integer satoshis."""
        return int(decimal.Decimal(str(amount)) * 100_000_000)

    @staticmethod
    def parse_tx_context(raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Injects calculated metadata into transaction objects."""
        context = {
            "id": CryptoTransformer.generate_fingerprint(raw_data),
            "raw_sum": sum(map(float, raw_data.values())) if isinstance(raw_data, dict) else 0.0,
            "version": "0.5.6-stable"
        }
        return {**raw_data, **context}