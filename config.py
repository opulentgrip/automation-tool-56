import json
import os
from collections import ChainMap
from pathlib import Path
from typing import Any, Dict

DEFAULT_CRYPTO_CONFIG: Dict[str, Any] = {
    "network": "ethereum-mainnet",
    "rpc_url": "https://cloudflare-eth.com",
    "gas_limit": 21000,
    "max_slippage_pct": 0.5,
    "trading_pairs": ["BTC/USDT", "ETH/USDT"],
    "retry_delay_sec": 3,
    "enable_mev_protection": True,
}


class ConfigError(Exception):
    """Raised when a configuration key cannot be resolved."""


class DynamicConfigLoader:
    def __init__(self, config_file: str = "crypto_config.json"):
        self.config_path = Path(config_file)
        self._store = ChainMap({}, self._load_file(), DEFAULT_CRYPTO_CONFIG)
        self._apply_env_overrides()

    def _load_file(self) -> Dict[str, Any]:
        if self.config_path.is_file():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                pass
        return {}

    def _apply_env_overrides(self) -> None:
        env_map: Dict[str, Any] = {}
        for key in DEFAULT_CRYPTO_CONFIG:
            env_key = f"CRYPTO_{key.upper()}"
            if env_key in os.environ:
                raw_val = os.environ[env_key]
                if raw_val.isdigit():
                    env_map[key] = int(raw_val)
                elif raw_val.replace(".", "", 1).isdigit():
                    env_map[key] = float(raw_val)
                elif raw_val.lower() in ("true", "false"):
                    env_map[key] = raw_val.lower() == "true"
                else:
                    env_map[key] = raw_val
        self._store.maps[0] = env_map

    def __getattr__(self, name: str) -> Any:
        if name in self._store:
            return self._store[name]
        raise ConfigError(f"Configuration key '{name}' does not exist")

    def __getitem__(self, item: str) -> Any:
        return self._store[item]

    def as_dict(self) -> Dict[str, Any]:
        return dict(self._store)
