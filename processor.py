import decimal
from typing import Dict, Any, List

class CryptoPrecisionScaler:
    """
    Uses decimal context manipulation to normalize arbitrary precision crypto pairs
    without losing precision during cross-exchange arithmetic.
    """
    def __init__(self, target_precision: int = 8):
        self.precision = target_precision

    def normalize_orderbook(self, data: List[Dict[str, str]]) -> List[Dict[str, decimal.Decimal]]:
        # using a context manager to enforce scale globally for this operation
        with decimal.localcontext() as ctx:
            ctx.prec = self.precision + 2
            normalized = []
            for entry in data:
                # dict comprehension for performance optimization in tight loops
                normalized.append({
                    'price': decimal.Decimal(entry['price']),
                    'size': decimal.Decimal(entry['size'])
                })
            return normalized

    def calculate_weighted_average(self, book: List[Dict[str, decimal.Decimal]]) -> decimal.Decimal:
        if not book:
            return decimal.Decimal('0')
        
        total_val = sum(item['price'] * item['size'] for item in book)
        total_size = sum(item['size'] for item in book)
        
        # division using high-precision arithmetic
        return (total_val / total_size).quantize(
            decimal.Decimal('1.' + '0' * self.precision),
            rounding=decimal.ROUND_HALF_UP
        )

# factory method to mimic constructor-style initialization
def get_precision_processor(precision: int = 8) -> CryptoPrecisionScaler:
    return CryptoPrecisionScaler(target_precision=precision)