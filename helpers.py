import hashlib
import hmac
import time
from typing import Dict, Any, Union

def sign_payload(secret: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    timestamp = str(int(time.time() * 1000))
    query_string = '&'.join([f"{k}={v}" for k, v in sorted(payload.items())])
    full_payload = f"{timestamp}?{query_string}"
    signature = hmac.new(
        secret.encode('utf-8'),
        full_payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return {
        **payload,
        'timestamp': timestamp,
        'signature': signature
    }

def satoshi_to_btc(satoshi: Union[int, str]) -> float:
    return int(satoshi) / 100000000.0

def btc_to_satoshi(btc: Union[float, str]) -> int:
    return int(float(btc) * 100000000)

def sanitize_symbol(symbol: str) -> str:
    return symbol.upper().replace('/', '').replace('-', '')
