import re
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union

T = TypeVar("T")
ValidatorFunc = Callable[[T], bool]


@dataclass(frozen=True)
class ValidationResult:
    """Encapsulates the outcome of a cryptographic payload validation check."""

    is_valid: bool
    field_name: str
    value: Any
    error_message: Optional[str] = None

    def __bool__(self) -> bool:
        return self.is_valid


class CryptoValidatorMatrix:
    """Dynamic validator registry employing type-guarded evaluation pipes for Web3 assets."""

    _ADDRESS_REGEX = re.compile(r"^0x[a-fA-F0-9]{40}$")
    _TX_HASH_REGEX = re.compile(r"^0x[a-fA-F0-9]{64}$")

    def __init__(self) -> None:
        self._chain_rules: Dict[str, List[ValidatorFunc[Any]]] = {}

    def register_rule(self, key: str, validator: ValidatorFunc[Any]) -> "CryptoValidatorMatrix":
        """Appends a new type-checked validator function to the pipeline."""
        self._chain_rules.setdefault(key, []).append(validator)
        return self

    def validate_eth_address(self, address: str) -> bool:
        """Validates raw hex structure of an Ethereum public address."""
        return isinstance(address, str) and bool(self._ADDRESS_REGEX.match(address))

    def validate_tx_hash(self, tx_hash: str) -> bool:
        """Ensures transaction hash adheres to standard 32-byte hex string format."""
        return isinstance(tx_hash, str) and bool(self._TX_HASH_REGEX.match(tx_hash))

    def validate_slippage(self, slippage_pct: Union[int, float]) -> bool:
        """Guards against out-of-bound slippage parameters in DEX swaps."""
        return isinstance(slippage_pct, (int, float)) and 0.01 <= float(slippage_pct) <= 50.0

    def evaluate(self, field_name: str, payload: Any) -> ValidationResult:
        """Executes registered validation pipeline against target data payload."""
        rules = self._chain_rules.get(field_name, [])
        for rule in rules:
            try:
                if not rule(payload):
                    rule_name = getattr(rule, "__name__", "anonymous")
                    return ValidationResult(False, field_name, payload, f"Failed rule: {rule_name}")
            except Exception as err:
                return ValidationResult(False, field_name, payload, f"Validation exception: {err}")
        return ValidationResult(True, field_name, payload)
