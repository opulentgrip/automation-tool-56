import re
from typing import Any, Dict

class CryptoValidator:
    SCHEMA = {
        'tx_hash': r'0x[a-fA-F0-9]{64}',
        'amount': r'^[0-9]*\.?[0-9]+$',
        'chain_id': r'^[0-9]{1,5}$'
    }

    @staticmethod
    def sanitize(data: Dict[str, Any]) -> bool:
        try:
            for key, pattern in CryptoValidator.SCHEMA.items():
                val = str(data.get(key, ''))
                if not re.match(pattern, val):
                    return False
            return float(data.get('amount', 0)) > 0
        except (ValueError, TypeError):
            return False

def validate_payload(func):
    def wrapper(*args, **kwargs):
        data = args[0] if args else kwargs.get('data', {})
        if not CryptoValidator.sanitize(data):
            raise ValueError(f'Malformed crypto payload detected: {data}')
        return func(*args, **kwargs)
    return wrapper

def run_safe_process(processor_func, data):
    if CryptoValidator.sanitize(data):
        return processor_func(data)
    return {'status': 'rejected', 'reason': 'validation_failed'}