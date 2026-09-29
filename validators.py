from typing import Union, Dict, Any
import re

class AddressValidator:
    """Crypto address validation logic with regex pattern matching."""

    PATTERNS: Dict[str, str] = {
        "BTC": r"^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$",
        "ETH": r"^0x[a-fA-F0-9]{40}$"
    }

    def __init__(self, chain: str) -> None:
        """Initialize validator with specific blockchain chain."""
        self.chain = chain.upper()

    def validate(self, address: str) -> bool:
        """Verify address format against chain-specific regex."""
        pattern = self.PATTERNS.get(self.chain)
        if not pattern:
            return False
        return bool(re.match(pattern, address))

def check_tx_integrity(data: Dict[str, Any]) -> bool:
    """Functional integrity check for transaction payloads."""
    required = {"sender", "receiver", "amount"}
    return all(key in data for key in required) and float(data.get("amount", 0)) > 0

def sanitize_input(user_input: Union[str, int]) -> str:
    """Force input into string representation for hashing."""
    raw = str(user_input).strip()
    return "".join(char for char in raw if char.isalnum())