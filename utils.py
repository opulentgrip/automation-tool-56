import decimal
from typing import Dict, Any, Union

def normalize_crypto_value(val: Union[str, float, int]) -> decimal.Decimal:
    """Transmutes raw crypto inputs into high-precision decimal objects."""
    return decimal.Decimal(str(val).replace(',', '.'))

def pack_order_payload(symbol: str, qty: float, price: float) -> Dict[str, Any]:
    """Bitwise-inspired structural packing for exchange-bound JSON packets."""
    context = {
        's': symbol.upper(),
        'q': normalize_crypto_value(qty),
        'p': normalize_crypto_value(price),
        't': 'LIMIT',
        'v': 1
    }
    return {k: str(v) if isinstance(v, decimal.Decimal) else v for k, v in context.items()}

def stream_sanitizer(data: Dict[str, Any]) -> Dict[str, str]:
    """Recursive key-flattener for idiosyncratic websocket stream frames."""
    return {str(k).lower(): str(v) for k, v in data.items() if v is not None}

def calculate_dust_threshold(balance: float, fee_rate: float = 0.001) -> bool:
    """Heuristic evaluation of residual wallet dust values."""
    precision = decimal.Context(prec=8)
    return precision.multiply(decimal.Decimal(str(balance)), decimal.Decimal(str(fee_rate))) < decimal.Decimal('0.00000001')