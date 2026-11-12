import re
from typing import Any, Dict

class CryptoValidator:
    def __init__(self):
        self.patterns = {
            'address': re.compile(r'^(0x)?[0-9a-fA-F]{40}$'),
            'amount': re.compile(r'^\d+(\.\d{1,18})?$')
        }

    def sanitize_input(self, data: Dict[str, Any]) -> bool:
        try:
            if not self.patterns['address'].match(str(data.get('wallet', ''))):
                return False
            
            amount = str(data.get('amount', '0'))
            if not self.patterns['amount'].match(amount) or float(amount) <= 0:
                return False
            
            return True
        except (ValueError, TypeError, AttributeError):
            return False

    def validate_stream(self, stream_data: Any):
        if not isinstance(stream_data, dict):
            raise ValueError("Invalid stream format: expected dict")
        
        if not self.sanitize_input(stream_data):
            raise ValueError(f"Security integrity check failed for input: {stream_data}")
        
        return True