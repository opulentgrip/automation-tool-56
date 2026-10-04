import os
import json
from pathlib import Path
from typing import Any, Dict

DEFAULT_CRYPTO_CONFIG: Dict[str, Any] = {
    "network": {
        "chain_id": 1,
        "rpc_url": "https://eth.llamarpc.com",
        "timeout_seconds": 15,
    },
    "trading": {
        "max_slippage_pct": 0.5,
        "gas_price_gwei": 30.0,
        "auto_hedge": False,
    },
    "security": {
        "verify_contracts": True,
        "min_confirmations": 2,
    }
}

class ConfigLoader:
    """Dynamic configuration loader with environment overrides and dict blending."""

    def __init__(self, config_path: str = "config.json"):
        self._path = Path(config_path)
        self._raw_config = self._load_and_merge()

    def _load_and_merge(self) -> Dict[str, Any]:
        file_cfg = {}
        if self._path.exists():
            with open(self._path, "r", encoding="utf-8") as f:
                file_cfg = json.load(f)

        merged = {}
        for section, defaults in DEFAULT_CRYPTO_CONFIG.items():
            user_section = file_cfg.get(section, {})
            merged[section] = defaults | user_section

            for key, default_val in defaults.items():
                env_var = f"CRYPTO_{section.upper()}_{key.upper()}"
                if env_var in os.environ:
                    val = os.environ[env_var]
                    target_type = type(default_val)
                    if target_type == bool:
                        merged[section][key] = val.lower() in ("true", "1", "yes")
                    else:
                        merged[section][key] = target_type(val)

        return merged

    def __getattr__(self, name: str) -> Any:
        if name in self._raw_config:
            val = self._raw_config[name]
            if isinstance(val, dict):
                return type("ConfigSection", (), {
                    "get": val.get,
                    **{k: v for k, v in val.items()}
                })()
            return val
        raise AttributeError(f"Configuration section '{name}' not found")

    def get(self, section: str, key: str, fallback: Any = None) -> Any:
        return self._raw_config.get(section, {}).get(key, fallback)
