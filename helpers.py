import hashlib
import hmac
from decimal import Decimal
from functools import reduce
from typing import Any, Callable, Union


class CryptoMath(type):
    """Metaclass providing dynamic unit conversion helpers via dynamic attribute lookup."""

    _CONVERSIONS = {
        "sats_to_btc": Decimal("0.00000001"),
        "btc_to_sats": Decimal("100000000"),
        "wei_to_eth": Decimal("1e-18"),
        "eth_to_wei": Decimal("1e18"),
        "gwei_to_eth": Decimal("1e-9"),
    }

    def __getattr__(cls, name: str) -> Callable[[Union[int, float, str]], Decimal]:
        if name in cls._CONVERSIONS:
            return lambda val: Decimal(str(val)) * cls._CONVERSIONS[name]
        raise AttributeError(f"Invalid unit converter: {name}")


class Units(metaclass=CryptoMath):
    """Fluent API helper for crypto unit conversions. e.g. Units.sats_to_btc(500000)"""

    pass


def pipe(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Functional helper to chain multiple transformations sequentially."""
    return lambda initial: reduce(lambda acc, f: f(acc), funcs, initial)


def make_signer(secret: str, algorithm: str = "sha256") -> Callable[[Union[str, bytes]], str]:
    """Creates a curried signing function using HMAC hashing."""
    key = secret.encode("utf-8")
    hash_fn = getattr(hashlib, algorithm)
    return lambda payload: hmac.new(
        key,
        payload if isinstance(payload, bytes) else str(payload).encode("utf-8"),
        hash_fn,
    ).hexdigest()


def sanitize_hex(raw_hex: str) -> str:
    """Normalizes hex strings with dynamic zero-padding rules."""
    stripped = raw_hex.strip().lower()
    clean = stripped[2:] if stripped.startswith("0x") else stripped
    padded = clean.zfill(len(clean) + (len(clean) % 2))
    return f"0x{padded}"


def format_tx_id(tx_hash: str, start: int = 6, end: int = 4) -> str:
    """Truncates long transaction hashes for logger output."""
    return f"{tx_hash[:start]}...{tx_hash[-end:]}" if len(tx_hash) > (start + end) else tx_hash
