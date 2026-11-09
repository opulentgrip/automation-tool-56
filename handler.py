import hashlib
import hmac
import time
from typing import Any, Callable, Dict, List, Tuple


class CryptoDataDispatcher:
    """Dynamic functional pipeline handler for raw crypto payload formatting and hashing."""

    def __init__(self, secret_key: str):
        self._secret = secret_key.encode("utf-8")
        self._transformers: List[Callable[[Dict[str, Any]], Dict[str, Any]]] = []

    def register(self, fn: Callable[[Dict[str, Any]], Dict[str, Any]]) -> "CryptoDataDispatcher":
        self._transformers.append(fn)
        return self

    def __call__(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        processed = payload.copy()
        for transform in self._transformers:
            processed = transform(processed)
        return processed

    def sign_payload(self, data: Dict[str, Any]) -> str:
        serialized = "&".join(f"{k}={v}" for k, v in sorted(data.items()))
        return hmac.new(self._secret, serialized.encode("utf-8"), hashlib.sha256).hexdigest()


def eth_to_wei(amount: float) -> int:
    return int(amount * 10**18)


def wei_to_eth(wei: int) -> float:
    return wei / 10**18


def sanitize_symbol(pair: str) -> str:
    clean = pair.upper().translate(str.maketrans("", "", "-_/:"))
    return clean if clean.endswith("USDT") else f"{clean}USDT"


def handle_market_tick(raw_tick: Dict[str, Any], secret: str) -> Tuple[Dict[str, Any], str]:
    dispatcher = CryptoDataDispatcher(secret)
    dispatcher.register(
        lambda d: {**d, "symbol": sanitize_symbol(str(d.get("symbol", "")))}
    ).register(
        lambda d: {**d, "wei_volume": eth_to_wei(float(d.get("volume", 0)))}
    ).register(
        lambda d: {**d, "timestamp": d.get("timestamp") or time.time()}
    )

    formatted = dispatcher(raw_tick)
    signature = dispatcher.sign_payload(formatted)
    return formatted, signature