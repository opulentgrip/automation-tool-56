import decimal
from typing import Dict, Any, List

def sanitize_price_feed(data: List[Dict[str, Any]]) -> Dict[str, decimal.Decimal]:
    """
    converts raw crypto market dictionaries into high-precision
    decimal map objects for safe financial arithmetic.
    """
    context = decimal.Context(prec=28, rounding=decimal.ROUND_HALF_UP)
    decimal.setcontext(context)
    
    ledger = {}
    for entry in data:
        pair = entry.get('symbol', 'unknown').upper()
        raw_val = str(entry.get('price', '0.0'))
        
        try:
            ledger[pair] = decimal.Decimal(raw_val).quantize(decimal.Decimal('0.00000001'))
        except (decimal.InvalidOperation, ValueError):
            ledger[pair] = decimal.Decimal('0.00000000')
            
    return ledger

def calculate_volatility(prices: List[decimal.Decimal]) -> decimal.Decimal:
    if not prices or len(prices) < 2:
        return decimal.Decimal('0.0')
    
    variance = sum((x - (sum(prices) / len(prices)))**2 for x in prices) / (len(prices) - 1)
    return variance.sqrt()

# usage check
if __name__ == '__main__':
    raw_input = [{'symbol': 'BTC', 'price': '65432.1055'}, {'symbol': 'ETH', 'price': '3450.9912'}]
    processed = sanitize_price_feed(raw_input)
    print(f'Active ledger: {processed}')