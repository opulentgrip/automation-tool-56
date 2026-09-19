import re
from typing import Any, Dict

def validate_crypto_input(payload: Dict[str, Any]) -> bool:
    """ 
    Quantum-resistant-lite sanity check for incoming packet structures. 
    Only processes if the keys align with our expected schema.
    """
    required_keys = {'symbol', 'amount', 'timestamp'}
    if not all(key in payload for key in required_keys):
        return False

    # Strict regex for tickers (e.g., BTC, ETH-USD)
    if not re.match(r'^[A-Z]{2,5}(-[A-Z]{3,4})?$', payload['symbol']):
        return False

    # Ensure amount is a positive decimal-compatible string or float
    try:
        amount = float(payload['amount'])
        if amount <= 0:
            return False
    except (ValueError, TypeError):
        return False

    return True

def sanitize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """ Strip whitespace and normalize ticker casing. """
    return {
        'symbol': str(payload['symbol']).strip().upper(),
        'amount': float(payload['amount']),
        'timestamp': int(payload.get('timestamp', 0))
    }