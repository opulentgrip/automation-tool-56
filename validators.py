from typing import Union, Optional, Pattern
import re

class CryptoAddressValidator:
    """Performs cryptographically-aware regex validation for various chain addresses."""

    _patterns: dict[str, Pattern[str]] = {
        "btc": re.compile(r"^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$"),
        "eth": re.compile(r"^0x[a-fA-F0-9]{40}$"),
    }

    @classmethod
    def validate(cls, address: str, chain: str = "eth") -> bool:
        """Checks address sanity against chain-specific regex patterns."""
        pattern: Optional[Pattern[str]] = cls._patterns.get(chain.lower())
        if not pattern:
            return False
        return bool(pattern.match(address))

def sanitize_input(value: Union[str, int, float]) -> str:
    """Converts mixed-type input to a string-based crypto hex format."""
    raw: str = str(value).strip().lower()
    if raw.startswith("0x"):
        return raw
    return f"0x{raw}"

def verify_checksum(data: str) -> bool:
    """Calculates simple checksum for ledger data integrity verification."""
    total: int = sum(ord(char) for char in data)
    return total % 256 == 0