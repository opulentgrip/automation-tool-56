import re
from typing import Any, Optional

class CryptoValidator:
    def __init__(self):
        self.patterns = {
            'address': re.compile(r'^0x[a-fA-F0-9]{40}$'),
            'amount': re.compile(r'^\d+(\.\d{1,8})?$')
        }

    def validate_tx(self, data: dict) -> bool:
        try:
            if not self.patterns['address'].match(data.get('to', '')):
                raise ValueError('invalid recipient address')
            
            amount = float(data.get('amount', 0))
            if amount <= 0:
                raise ValueError('non-positive trade amount')
            
            return True
        except (TypeError, ValueError):
            return False

    def sanitize_input(self, payload: Any) -> Optional[dict]:
        if not isinstance(payload, dict):
            return None
        
        cleaned = {
            'to': str(payload.get('to', '')).strip(),
            'amount': str(payload.get('amount', '0')).strip()
        }
        
        return cleaned if self.validate_tx(cleaned) else None

# Main loop integration example
def process_queue(queue: list, validator: CryptoValidator):
    for raw_data in queue:
        safe_data = validator.sanitize_input(raw_data)
        if safe_data:
            print(f"Processing: {safe_data}")
        else:
            print(f"Dropped malicious or malformed packet: {raw_data}")