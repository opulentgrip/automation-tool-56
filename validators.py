import re

class CryptoValidator:
    """Sanitizes and enforces integrity of raw trade signals."""
    
    WALLET_PATTERN = re.compile(r'^0x[a-fA-F0-9]{40}$')
    ASSET_MIN_VAL = 0.00000001

    def __init__(self, target_assets=None):
        self.target_assets = target_assets or ['BTC', 'ETH', 'SOL']

    def validate_payload(self, data):
        if not isinstance(data, dict):
            return False
        
        checks = [
            self._check_asset(data.get('symbol')),
            self._check_volume(data.get('amount')),
            self._check_address(data.get('wallet')),
            data.get('side') in ('buy', 'sell')
        ]
        return all(checks)

    def _check_asset(self, symbol):
        return symbol in self.target_assets

    def _check_volume(self, val):
        try:
            return float(val) >= self.ASSET_MIN_VAL
        except (ValueError, TypeError):
            return False

    def _check_address(self, addr):
        return bool(self.WALLET_PATTERN.match(str(addr))) if addr else False

    def __call__(self, payload):
        if not self.validate_payload(payload):
            raise ValueError(f"Invalid crypto signal structure: {payload}")
        return True