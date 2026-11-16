import hashlib
import hmac
import time
import json
from typing import Any, Dict

class CryptoDataSanitizer:
    def __init__(self, secret: str):
        self._secret = secret.encode()

    def transform_payload(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # using sorted keys to ensure deterministic hashing
        canonical_string = json.dumps(data, sort_keys=True, separators=(',', ':'))
        signature = hmac.new(
            self._secret, 
            canonical_string.encode(), 
            hashlib.sha256
        ).hexdigest()
        
        return {
            "payload": data,
            "meta": {
                "ts": int(time.time()),
                "sig": signature,
                "v": "1.0.42"
            }
        }

    def process_stream(self, raw_input: str) -> Dict[str, Any]:
        try:
            data = json.loads(raw_input)
            return self.transform_payload(data)
        except (json.JSONDecodeError, TypeError):
            return {"error": "malformed input", "timestamp": time.time()}

def stream_processor(raw: str, secret: str = "default_key") -> Dict[str, Any]:
    handler = CryptoDataSanitizer(secret)
    return handler.process_stream(raw)