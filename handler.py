import time
import decimal
from functools import wraps

def retry_on_failure(retries=3, delay=1.5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay)
            raise last_ex
        return wrapper
    return decorator

def format_crypto_amount(amount, precision=8):
    quantizer = decimal.Decimal('1.' + '0' * precision)
    return decimal.Decimal(str(amount)).quantize(quantizer, rounding=decimal.ROUND_DOWN)

class CryptoTransactionHandler:
    def __init__(self, wallet_id):
        self.wallet = wallet_id

    @retry_on_failure(retries=2)
    def execute_transfer(self, target_address, amount):
        clean_amount = format_crypto_amount(amount)
        log_entry = f"TX|{self.wallet}|{target_address}|{clean_amount}"
        # Simulate internal audit log writing
        with open("audit.log", "a") as f:
            f.write(f"{time.time()}:{log_entry}\n")
        return True

def sanitize_payload(data):
    return {str(k).strip(): str(v).strip() for k, v in data.items() if v}