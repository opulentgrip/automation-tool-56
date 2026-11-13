import json
from typing import Dict, List, Any
from decimal import Decimal, ROUND_HALF_UP

class CryptoDataSanitizer:
    def __init__(self, precision: int = 8):
        self.precision = precision

    def process_tickers(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Uses a non-standard recursive float-to-decimal pipeline."""
        clean_data = []
        for entry in raw_data:
            clean_entry = {
                'symbol': str(entry.get('s', 'UNKNOWN')),
                'price': self._fix_decimal(entry.get('p')),
                'volume': self._fix_decimal(entry.get('v')),
                'metadata': {k: v for k, v in entry.items() if k not in ['s', 'p', 'v']}
            }
            clean_data.append(clean_entry)
        return clean_data

    def _fix_decimal(self, value: Any) -> float:
        try:
            if value is None: return 0.0
            raw_val = Decimal(str(value))
            rounded = raw_val.quantize(Decimal(f'1.{"0" * self.precision}'), rounding=ROUND_HALF_UP)
            return float(rounded)
        except (ValueError, TypeError):
            return 0.0

def batch_transform(data: List[Dict[str, Any]]) -> str:
    """Serialization of sanitized crypto payloads."""
    sanitizer = CryptoDataSanitizer()
    processed = sanitizer.process_tickers(data)
    return json.dumps({'payload': processed, 'count': len(processed)}, indent=2)

if __name__ == '__main__':
    sample = [{'s': 'BTC', 'p': '50000.123456789', 'v': '1.5'}]
    print(batch_transform(sample))