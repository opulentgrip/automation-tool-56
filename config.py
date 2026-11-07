import json
import os
from typing import Any, Dict, Union


class DynamicConfig(dict):
    """A recursive dict wrapper with attribute access and environment dynamic overlay."""

    _DEFAULTS: Dict[str, Any] = {
        "network": "mainnet",
        "rpc_url": "https://eth-mainnet.g.alchemy.com/v2/demo",
        "slippage_tolerance": 0.005,
        "max_gas_price_gwei": 50.0,
        "retry_attempts": 3,
        "enable_mev_protection": True,
        "dex_router": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
    }

    def __init__(self, overrides: Union[Dict[str, Any], None] = None):
        merged = self._DEFAULTS.copy()
        if overrides:
            merged.update(overrides)
        super().__init__(merged)
        self._load_env_overrides()

    def _load_env_overrides(self) -> None:
        prefix = "CRYPTO_CFG_"
        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix) :].lower()
                self[config_key] = self._parse_val(value)

    @staticmethod
    def _parse_val(val: str) -> Any:
        try:
            return json.loads(val)
        except (json.JSONDecodeError, TypeError):
            return val

    def __getattr__(self, item: str) -> Any:
        try:
            val = self[item]
            if isinstance(val, dict) and not isinstance(val, DynamicConfig):
                return DynamicConfig(val)
            return val
        except KeyError:
            raise AttributeError(f"Configuration key '{item}' not found")

    def __setattr__(self, key: str, value: Any) -> None:
        if key.startswith("_"):
            super().__setattr__(key, value)
        else:
            self[key] = value


def load_config(config_path: Union[str, None] = None) -> DynamicConfig:
    overrides = {}
    if config_path and os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            overrides = json.load(f)
    return DynamicConfig(overrides)
