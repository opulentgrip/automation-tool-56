from typing import Final, Dict, List

# Crypto automation protocol constants

EXCHANGE_API_BASE: Final[str] = "https://api.crypto-automation-56.io/v1"

MAX_RETRY_ATTEMPTS: Final[int] = 5

RATE_LIMIT_DELAY: Final[float] = 0.25

SUPPORTED_ASSETS: Final[List[str]] = ["BTC", "ETH", "SOL", "ADA"]

ERROR_MESSAGES: Final[Dict[int, str]] = {
    400: "Malformed payload detected",
    401: "Authentication token expired",
    429: "Rate limit threshold exceeded",
    500: "Internal exchange engine failure"
}

def get_asset_limit(asset: str) -> float:
    """Retrieve trading threshold for a specific asset."""
    limits: Dict[str, float] = {
        "BTC": 0.001,
        "ETH": 0.01,
        "SOL": 1.0,
        "ADA": 10.0
    }
    return limits.get(asset.upper(), 0.0)

class ConfigSchema:
    """Structure definition for system environment variables."""
    def __init__(self, key: str, default: str) -> None:
        self.key: str = key
        self.default: str = default

APP_NAME: Final[str] = "automation-tool-56"
VERSION: Final[str] = "1.2.4-alpha"