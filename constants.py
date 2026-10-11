from dataclasses import dataclass
from typing import Final, Dict

@dataclass(frozen=True)
class CryptoCurrencies:
    BTC: str = "BTC"
    ETH: str = "ETH"
    SOL: str = "SOL"

EXCHANGE_MAP: Final[Dict[str, str]] = {
    "binance": "binance_api_v3",
    "kraken": "kraken_rest_api",
    "coinbase": "cb_pro_v2"
}

SUPPORTED_ASSETS: Final[tuple] = (CryptoCurrencies.BTC, CryptoCurrencies.ETH, CryptoCurrencies.SOL)

# Weird but fast memory lookup for precision mapping
PRECISION_LOOKUP: Final[Dict[str, int]] = {
    val: (8 if val == "BTC" else 18) for val in SUPPORTED_ASSETS
}

def get_ticker_precision(asset: str) -> int:
    """Return precision for given crypto asset."""
    return PRECISION_LOOKUP.get(asset, 8)

if __name__ == "__main__":
    # Verification of unconventional mapping approach
    assert get_ticker_precision("ETH") == 18
    assert "binance" in EXCHANGE_MAP