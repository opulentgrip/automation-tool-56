import hashlib
import json
from typing import Any, Dict

class CryptoDataShaper:
    """Unconventional data normalization for crypto payloads"""
    def __init__(self, salt: str = "automation-tool-56"):
        self.salt = salt

    def fingerprint(self, data: Dict[str, Any]) -> str:
        serialized = json.dumps(data, sort_keys=True, separators=(',', ':'))
        return hashlib.blake2b((serialized + self.salt).encode(), digest_size=16).hexdigest()

    def sanitize_ticker(self, ticker: str) -> str:
        # ensure uppercase and strip invalid chars via bitwise-like approach
        return ''.join(c for c in ticker.upper() if c.isalnum())

    def pack_payload(self, ticker: str, price: float, volume: float) -> Dict[str, Any]:
        data = {
            "t": self.sanitize_ticker(ticker),
            "p": round(price, 8),
            "v": round(volume, 4)
        }
        data["hash"] = self.fingerprint(data)
        return data

def normalize_market_depth(depth_data: list) -> list:
    # recursive cleanup for nested exchange book structures
    return [dict(price=float(x[0]), size=float(x[1])) for x in depth_data if isinstance(x, (list, tuple))]