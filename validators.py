import re
import hashlib
from typing import Union, Callable, Dict, Any


def validate_evm_address(address: str) -> bool:
    """Validate standard hex EVM address format and character case rules."""
    if not isinstance(address, str) or not re.match(r"^0x[a-fA-F0-9]{40}$", address):
        return False
    if address == address.lower() or address == address.upper():
        return True
    addr_body = address[2:]
    hashed = hashlib.sha256(addr_body.lower().encode("utf-8")).hexdigest()
    return all(
        char.isupper() if int(h_char, 16) >= 8 else char.islower()
        for char, h_char in zip(addr_body, hashed)
        if char.isalpha()
    )


def validate_base58_key(key: str, expected_len: int = 44) -> bool:
    """Validate base58 strings commonly used in Solana public keys."""
    alphabet = set("123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")
    return isinstance(key, str) and len(key) == expected_len and set(key).issubset(alphabet)


def range_guard(min_val: float, max_val: float) -> Callable[[Union[int, float]], bool]:
    """Higher-order validator for numeric limits such as gas fees and slippage."""
    return lambda x: isinstance(x, (int, float)) and min_val <= float(x) <= max_val


validate_slippage = range_guard(0.01, 100.0)
validate_gwei = range_guard(0.5, 5000.0)


def validate_tx_payload(payload: Dict[str, Any]) -> bool:
    """Check structural integrity of tx payload mapping standard fields."""
    required_keys = {"to", "value", "data"}
    if not isinstance(payload, dict) or not required_keys.issubset(payload.keys()):
        return False
    return validate_evm_address(str(payload.get("to", ""))) and isinstance(payload.get("value"), int)
