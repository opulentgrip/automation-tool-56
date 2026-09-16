import hashlib
from typing import Union, Dict

class CryptoVal:
    """Dynamic converter for crypto units utilizing dynamic attributes."""
    UNITS: Dict[str, int] = {
        "wei": 0,
        "gwei": 9,
        "ether": 18,
        "satoshi": 0,
        "btc": 8,
    }

    def __init__(self, value: Union[int, float, str], unit: str = "ether"):
        self.raw_value = float(value)
        self.unit = unit.lower()

    def to_unit(self, target_unit: str) -> float:
        target = target_unit.lower()
        if self.unit not in self.UNITS or target not in self.UNITS:
            raise ValueError(f"Unsupported unit transition: {self.unit} to {target}")
        
        # Convert to base representation, then scale to target unit
        base_val = self.raw_value * (10 ** self.UNITS[self.unit])
        return base_val / (10 ** self.UNITS[target])

    def __getattr__(self, name: str) -> float:
        if name.startswith("to_"):
            target = name.replace("to_", "", 1)
            return self.to_unit(target)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

def base58_encode(data: bytes) -> str:
    """Encodes raw bytes to a base58 string for address creation."""
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    num = int.from_bytes(data, byteorder="big")
    res = []
    while num > 0:
        num, mod = divmod(num, 58)
        res.append(alphabet[mod])
    
    pad = len(data) - len(data.lstrip(b'\x00'))
    return "1" * pad + "".join(reversed(res))

def secure_checksum(payload: bytes) -> str:
    """Generates double SHA-256 checksum slice for address verification."""
    first_hash = hashlib.sha256(payload).digest()
    second_hash = hashlib.sha256(first_hash).digest()
    return second_hash[:4].hex()
