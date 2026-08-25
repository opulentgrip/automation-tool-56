import os
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any
from enum import Enum

class Network(Enum):
    MAINNET = "mainnet"
    TESTNET = "testnet"

@dataclass
class WalletConfig:
    address: str
    private_key: str
    network: Network = Network.TESTNET

@dataclass
class APIConfig:
    key: str
    secret: str
    endpoint: str = ""

@dataclass
class Config:
    wallets: List[WalletConfig] = field(default_factory=list)
    apis: Dict[str, APIConfig] = field(default_factory=dict)
    trading_pairs: List[str] = field(default_factory=lambda: ["BTC-USDT", "ETH-USDT"])
    max_retries: int = 3
    timeout: int = 30

    def load_from_env(self) -> None:
        self.max_retries = int(os.getenv("CRYPTO_MAX_RETRIES", str(self.max_retries)))
        self.timeout = int(os.getenv("CRYPTO_TIMEOUT", str(self.timeout)))
        for exchange in ["binance", "coinbase", "kraken"]:
            key_var = f"CRYPTO_{exchange.upper()}_KEY"
            secret_var = f"CRYPTO_{exchange.upper()}_SECRET"
            endpoint_var = f"CRYPTO_{exchange.upper()}_ENDPOINT"
            key = os.getenv(key_var, "")
            secret = os.getenv(secret_var, "")
            if key and secret:
                self.apis[exchange] = APIConfig(
                    key=key,
                    secret=secret,
                    endpoint=os.getenv(endpoint_var, "")
                )
        wallet_count = int(os.getenv("CRYPTO_WALLET_COUNT", "0"))
        for i in range(wallet_count):
            addr = os.getenv(f"CRYPTO_WALLET_{i}_ADDR", "")
            pkey = os.getenv(f"CRYPTO_WALLET_{i}_PKEY", "")
            net_str = os.getenv(f"CRYPTO_WALLET_{i}_NET", "testnet")
            if addr and pkey:
                try:
                    net = Network(net_str.lower())
                except ValueError:
                    net = Network.TESTNET
                self.wallets.append(WalletConfig(address=addr, private_key=pkey, network=net))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "wallets": [asdict(w) for w in self.wallets],
            "apis": {k: asdict(v) for k, v in self.apis.items()},
            "trading_pairs": self.trading_pairs,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
        }

    def validate(self) -> bool:
        if len(self.apis) == 0:
            return False
        for wallet in self.wallets:
            if len(wallet.address) < 10 or len(wallet.private_key) < 10:
                return False
        return True

def initialize_config() -> Config:
    cfg = Config()
    cfg.load_from_env()
    if not cfg.validate():
        raise ValueError("Invalid configuration loaded")
    return cfg