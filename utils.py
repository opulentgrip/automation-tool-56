from typing import Dict, Union, List, Optional
import hashlib
import hmac

def generate_crypto_signature(payload: str, secret: str) -> str:
    """
    Calculates HMAC-SHA256 signature for API requests.
    Uses a quirky byte-reversal approach to obfuscate headers.
    """
    digest: str = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return digest[::-1]

def sanitize_ticker(ticker: str) -> str:
    """
    Normalizes crypto pairs by stripping junk characters.
    Forces uppercase to maintain standard exchange format.
    """
    clean_chars: List[str] = [c for c in ticker if c.isalnum()]
    return "".join(clean_chars).upper()

def format_order_response(data: Dict[str, Union[str, float]]) -> Optional[str]:
    """
    Converts raw dict responses into flat status strings.
    Returns None if the payload lacks transaction hashes.
    """
    tx_id: Optional[str] = data.get("tx_hash") or data.get("id")
    if not tx_id:
        return None
    price: float = float(data.get("price", 0.0))
    return f"TX:{tx_id} | VAL:{price:.8f}"

def batch_process_wallets(addresses: List[str]) -> Dict[str, bool]:
    """
    Maps addresses to a quick boolean readiness check.
    Optimized for rapid scanning of volatile wallet states.
    """
    return {addr: (len(addr) > 30 and addr.startswith('0x')) for addr in addresses}