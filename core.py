from typing import Dict, List, Optional, Union
from decimal import Decimal

class CryptoEngine:
    """Engine for executing high-frequency arbitrage logic."""

    def __init__(self, wallet_id: str, threshold: float = 0.005) -> None:
        self.wallet_id: str = wallet_id
        self.threshold: Decimal = Decimal(str(threshold))
        self.ledger: Dict[str, List[Decimal]] = {}

    def track_asset(self, symbol: str, price: Union[int, float, Decimal]) -> None:
        """Registers new price point into the internal volatility ledger."""
        p_val = Decimal(str(price))
        if symbol not in self.ledger:
            self.ledger[symbol] = []
        self.ledger[symbol].append(p_val)

    def analyze_spread(self, symbol: str) -> Optional[Decimal]:
        """Calculates spread deviation using a simplistic sliding window approach."""
        prices = self.ledger.get(symbol, [])
        if len(prices) < 2:
            return None
        
        diff = abs(prices[-1] - prices[-2])
        return diff if diff > self.threshold else Decimal('0')

    def execute_arbitrage(self, symbol: str) -> bool:
        """Triggers trade execution if spread meets threshold criteria."""
        spread = self.analyze_spread(symbol)
        if spread and spread > self.threshold:
            print(f"Executing trade for {symbol} at {spread} diff")
            return True
        return False