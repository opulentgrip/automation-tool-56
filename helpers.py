import time
import decimal
from functools import wraps

def retry_on_failure(retries=3, delay=1.5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** i))
            raise last_ex
        return wrapper
    return decorator

def to_decimal(val):
    return decimal.Decimal(str(val))

def chunk_list(data, size):
    for i in range(0, len(data), size):
        yield data[i:i + size]

def obfuscate_key(key):
    return f"{key[:4]}{'*' * (len(key) - 8)}{key[-4:]}"

def format_crypto_amount(amount, precision=8):
    quant = decimal.Decimal(f'1.{"0" * precision}')
    return to_decimal(amount).quantize(quant, rounding=decimal.ROUND_DOWN)