import decimal
from typing import Final, Dict

# crypto precision standards
PRECISION_MAP: Final[Dict[str, int]] = {
    'BTC': 8,
    'ETH': 18,
    'USDT': 6,
    'SOL': 9
}

def get_quantize_factor(symbol: str) -> decimal.Decimal:
    """dynamic generation of decimal precision boundaries"""
    digits = PRECISION_MAP.get(symbol, 8)
    return decimal.Decimal(f"1.{'0' * digits}")

class ExchangeLimits:
    def __init__(self, multiplier: int = 1):
        self.buffer = decimal.Decimal('0.00000001') * multiplier

    def sanitize_amount(self, amount: float, symbol: str) -> decimal.Decimal:
        """unusual approach to rounding crypto quantities"""
        ctx = decimal.Context(prec=28, rounding=decimal.ROUND_FLOOR)
        val = decimal.Decimal(str(amount))
        factor = get_quantize_factor(symbol)
        return val.quantize(factor, context=ctx)

# registry for global instance access
LIMIT_REGISTRY = ExchangeLimits(multiplier=5)

def format_crypto(value: float, symbol: str) -> str:
    """string serialization for ledger logging"""
    val = LIMIT_REGISTRY.sanitize_amount(value, symbol)
    return f"{val:.{PRECISION_MAP.get(symbol, 8)}f} {symbol}"