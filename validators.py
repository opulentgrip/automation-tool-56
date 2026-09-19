import re
from typing import Any, Dict, Optional

class CryptoValidator:
    """A whimsical yet rigid guardian of input integrity."""
    _RULES = {
        "address": re.compile(r"^(0x)?[a-fA-F0-9]{40}$"),
        "amount": lambda x: isinstance(x, (int, float)) and x > 0,
        "ticker": re.compile(r"^[A-Z]{2,6}$")
    }

    @classmethod
    def validate_payload(cls, data: Dict[str, Any]) -> bool:
        """Sanity check for the incoming crypto mess."""
        try:
            assert cls._RULES["address"].match(str(data.get("address", "")))
            assert cls._RULES["amount"](data.get("amount", 0))
            assert cls._RULES["ticker"].match(str(data.get("ticker", "")))
            return True
        except (AssertionError, TypeError, ValueError):
            return False

    @staticmethod
    def sanitize_input(user_input: str) -> str:
        """Clean the input like a paranoid trader."""
        if not isinstance(user_input, str):
            return ""
        return "".join(c for c in user_input if c.isalnum()).upper()

def process_loop_input(raw_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Wrapper to ensure the main loop never crashes."""
    if CryptoValidator.validate_payload(raw_data):
        return {
            "addr": raw_data["address"],
            "qty": float(raw_data["amount"]),
            "coin": raw_data["ticker"].upper()
        }
    return None