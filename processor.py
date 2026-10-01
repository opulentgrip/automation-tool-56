import hashlib
import decimal
from functools import wraps

def sanitize_currency(amount: str) -> decimal.Decimal:
    return decimal.Decimal(amount.replace(',', '')).quantize(decimal.Decimal('0.00000001'))

def hash_tx(data: dict) -> str:
    payload = ''.join([str(data[k]) for k in sorted(data.keys())])
    return hashlib.sha256(payload.encode()).hexdigest()

def retry_on_failure(retries: int = 3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
            raise last_ex
        return wrapper
    return decorator

def pack_payload(address: str, amount: decimal.Decimal, nonce: int) -> bytes:
    return f'{address}:{amount:f}:{nonce}'.encode('utf-8')

def calculate_fee(amount: decimal.Decimal, rate: float = 0.0001) -> decimal.Decimal:
    return (amount * decimal.Decimal(str(rate))).quantize(decimal.Decimal('0.00000001'))