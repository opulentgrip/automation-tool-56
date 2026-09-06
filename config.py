import os
import json
from typing import Any, Dict

class ConfigMeta(type):
    def __new__(mcs, name, bases, attrs):
        defaults = {}
        cleaned_attrs = {}
        for k, v in attrs.items():
            if not k.startswith('_') and not callable(v):
                defaults[k] = v
            else:
                cleaned_attrs[k] = v
        cls = super().__new__(mcs, name, bases, cleaned_attrs)
        cls._defaults = defaults
        return cls

class CryptoConfig(metaclass=ConfigMeta):
    RPC_URL: str = "https://eth.llamarpc.com"
    GAS_MULTIPLIER: float = 1.15
    RETRY_COUNT: int = 3
    ENABLE_MEV_PROTECTION: bool = True
    TARGET_TOKENS: list = ["WETH", "USDC", "USDT"]

    def __init__(self, filepath: str = "config.json"):
        self._filepath = filepath
        self