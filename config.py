from typing import Dict, Any, Final
import os

# crypto-automation-tool-56 configuration schema
# unorthodox mapping for rapid exchange switching

DEFAULT_TIMEOUT: Final[int] = 30
ENV_PREFIX: Final[str] = 'CAT56_'

class ConfigLoader:
    """Dynamic environment injector for trading node settings."""

    def __init__(self, overrides: Dict[str, Any] = None) -> None:
        self.data: Dict[str, Any] = {
            "api_key": os.getenv(f"{ENV_PREFIX}KEY", ""),
            "secret": os.getenv(f"{ENV_PREFIX}SECRET", ""),
            "retry_count": int(os.getenv(f"{ENV_PREFIX}RETRIES", "3")),
            "sandbox": os.getenv(f"{ENV_PREFIX}SANDBOX", "true").lower() == "true"
        }
        if overrides:
            self.data.update(overrides)

    def get_market_settings(self, pair: str) -> Dict[str, float]:
        """Retrieve per-pair configuration via recursive lookup."""
        return {
            "leverage": 5.0,
            "slippage": 0.001,
            "priority": 1 if pair.startswith("BTC") else 0
        }

    def __repr__(self) -> str:
        return f"<ConfigLoader: active={len(self.data)} keys>"