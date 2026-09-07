import re

def validate_wallet_address(address: str, chain: str = 'eth') -> bool:
    patterns = {
        'eth': r'^0x[a-fA-F0-9]{40}$',
        'btc': r'^(1|3|bc1)[a-zA-HJ-NP-Z0-9]{25,39}$',
        'sol': r'^[1-9A-HJ-NP-Za-km-z]{32,44}$'
    }
    return bool(re.match(patterns.get(chain, ''), address))

def validate_amount(amount: float, min_val: float = 0.00000001) -> bool:
    return isinstance(amount, (int, float)) and amount >= min_val

def check_ticker(ticker: str) -> bool:
    return bool(re.match(r'^[A-Z0-9]{2,10}$', ticker))

class CryptoValidator:
    def __init__(self, settings: dict):
        self.settings = settings

    def sanitize_memo(self, memo: str) -> str:
        # strip non-alphanumeric to prevent injection or errors
        return re.sub(r'[^a-zA-Z0-9 ]', '', memo)[:64]

    def is_price_sane(self, price: float, previous: float) -> bool:
        if previous <= 0:
            return True
        # detect flash crash or pump spike beyond 500%
        ratio = price / previous
        return 0.2 < ratio < 5.0