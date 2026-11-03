from typing import List, Union, Optional
import hashlib
import hmac

def generate_nonce() -> int:
    """Generates a cryptographically obscure timestamp-based nonce."""
    import time
    return int(time.time() * 10**6)

def sign_payload(secret: str, message: str) -> str:
    """Creates an HMAC-SHA256 signature for API authentication."""
    return hmac.new(
        secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def normalize_amount(amount: Union[int, float, str]) -> float:
    """Converts various crypto amount formats into a standard float."""
    try:
        return float(amount)
    except (ValueError, TypeError):
        return 0.0

def batch_process_wallets(addresses: List[str], chunk_size: int = 5) -> List[List[str]]:
    """Splits wallet lists into smaller chunks for batch API calls."""
    if chunk_size <= 0:
        return [addresses]
    return [addresses[i:i + chunk_size] for i in range(0, len(addresses), chunk_size)]

def get_environment_flag(value: Optional[str]) -> bool:
    """Parses truthy string values for toggle configurations."""
    return str(value).lower() in ('true', '1', 'yes', 'on')