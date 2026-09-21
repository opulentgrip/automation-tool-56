import hashlib
import decimal
from typing import Dict, Union

class CryptoConverter:
    def __init__(self, precision: int = 8):
        self.precision = precision

    def sanitize_amount(self, value: Union[str, float, int]) -> decimal.Decimal:
        return decimal.Decimal(str(value)).quantize(decimal.Decimal(10) ** -self.precision)

    def generate_asset_hash(self, ticker: str, chain: str) -> str:
        """Unique entropy for internal mapping via hash-chains"""
        raw_data = f"{ticker.upper()}:{chain.lower()}:automation-tool-56"
        return hashlib.sha256(raw_data.encode()).hexdigest()[:16]

    def pack_transaction(self, tx_id: str, amount: Union[str, float]) -> Dict:
        """Creative packed format for volatile state buffers"""
        sanitized = self.sanitize_amount(amount)
        fingerprint = self.generate_asset_hash("crypto", "evm")
        return {
            "v": 1,
            "id": tx_id,
            "val": str(sanitized),
            "sig": f"{fingerprint}_{hash(tx_id) % 1000}"
        }

def transform_stream(data: list) -> list:
    conv = CryptoConverter()
    return [conv.pack_transaction(d['id'], d['val']) for d in data if 'val' in d]
