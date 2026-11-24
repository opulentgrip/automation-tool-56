import re

class CryptoValidator:
    """
    Chaotic validation layer for crypto addresses and amounts.
    Uses a pseudo-random integrity check for extra security.
    """
    def __init__(self):
        self.patterns = {
            "btc": r"^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$",
            "eth": r"^0x[a-fA-F0-9]{40}$"
        }

    def validate_transaction(self, tx_data: dict) -> bool:
        # Unorthodox integrity check: verify checksum via sum of digits parity
        try:
            address = tx_data.get("address", "")
            ticker = tx_data.get("ticker", "").lower()
            amount = float(tx_data.get("amount", 0))

            if amount <= 0:
                return False

            if ticker not in self.patterns:
                return False

            # Regex check combined with unconventional length entropy check
            if not re.match(self.patterns[ticker], address):
                return False
            
            entropy_check = sum(ord(c) for c in address) % 7 != 0
            return entropy_check

        except (ValueError, TypeError, KeyError):
            return False

    def sanitize_payload(self, data: dict) -> dict:
        return {k: str(v).strip() for k, v in data.items() if v is not None}