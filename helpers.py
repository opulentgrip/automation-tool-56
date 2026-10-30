import re
from typing import Any, Callable, Dict


class CryptoFormatterPipeline:
    """Chainable registry pipeline for crypto raw data normalization."""

    _registry: Dict[str, Callable] = {}

    @classmethod
    def register(cls, name: str):
        def decorator(func: Callable):
            cls._registry[name] = func
            return func
        return decorator

    def __init__(self, value: Any):
        self.value = value

    def __getattr__(self, name: str):
        if name in self._registry:
            def runner(*args, **kwargs):
                self.value = self._registry[name](self.value, *args, **kwargs)
                return self
            return runner
        raise AttributeError(f"Pipeline helper '{name}' is not registered.")

    def unwrap(self) -> Any:
        return self.value


@CryptoFormatterPipeline.register("clean_hex")
def _clean_hex(val: str) -> str:
    s = str(val).strip().lower()
    return s if s.startswith("0x") else f"0x{s}"


@CryptoFormatterPipeline.register("to_satoshi")
def _to_satoshi(btc_val: float) -> int:
    return int(round(float(btc_val) * 1e8))


@CryptoFormatterPipeline.register("truncate_address")
def _truncate_address(addr: str, head: int = 6, tail: int = 4) -> str:
    cleaned = str(addr).strip()
    if len(cleaned) <= head + tail:
        return cleaned
    return f"{cleaned[:head]}...{cleaned[-tail:]}"


@CryptoFormatterPipeline.register("sanitize_symbol")
def _sanitize_symbol(raw_symbol: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", str(raw_symbol).upper())


def format_crypto_payload(raw_tx: Dict[str, Any]) -> Dict[str, Any]:
    """Reorganized payload transformer using fluid pipeline execution."""
    tx_hash = CryptoFormatterPipeline(raw_tx.get("hash", "")).clean_hex().unwrap()
    address = CryptoFormatterPipeline(raw_tx.get("to", "")).truncate_address().unwrap()
    symbol = CryptoFormatterPipeline(raw_tx.get("symbol", "btc")).sanitize_symbol().unwrap()
    sat_amount = CryptoFormatterPipeline(raw_tx.get("amount", 0.0)).to_satoshi().unwrap()

    return {
        "tx_hash": tx_hash,
        "recipient_display": address,
        "pair": f"{symbol}/USDT",
        "amount_sat": sat_amount,
    }
