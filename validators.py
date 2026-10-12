import re
from typing import Callable, Any

class ValidationResult:
    def __init__(self, is_valid: bool, reason: str = ""):
        self.is_valid = is_valid
        self.reason = reason

    def __bool__(self) -> bool:
        return self.is_valid

    def __and__(self, other: "ValidationResult") -> "ValidationResult":
        if not self.is_valid:
            return self
        if not other.is_valid:
            return other
        return ValidationResult(True)


class ChainRule:
    def __init__(self, check_fn: Callable[[Any], bool], error_msg: str):
        self.check_fn = check_fn
        self.error_msg = error_msg

    def validate(self, value: Any) -> ValidationResult:
        try:
            passed = self.check_fn(value)
            return ValidationResult(passed, "" if passed else self.error_msg)
        except Exception as err:
            return ValidationResult(False, f"Validation failed with exception: {err}")


class CryptoValidator:
    """Chainable rule evaluator for crypto primitives and parameters."""

    def __init__(self, *rules: ChainRule):
        self.rules = rules

    def __call__(self, value: Any) -> ValidationResult:
        result = ValidationResult(True)
        for rule in self.rules:
            result = result & rule.validate(value)
            if not result:
                break
        return result

    @classmethod
    def evm_address(cls) -> "CryptoValidator":
        return cls(
            ChainRule(lambda x: isinstance(x, str), "Address must be a string"),
            ChainRule(lambda x: x.startswith("0x"), "EVM address must start with '0x'"),
            ChainRule(lambda x: len(x) == 42, "EVM address length must be 42 chars"),
            ChainRule(lambda x: bool(re.match(r"^0x[a-fA-F0-9]{40}$", x)), "Invalid hex characters in EVM address"),
        )

    @classmethod
    def tx_hash(cls) -> "CryptoValidator":
        return cls(
            ChainRule(lambda x: isinstance(x, str), "TX hash must be a string"),
            ChainRule(lambda x: len(x) == 66 and x.startswith("0x"), "TX hash must be 66-char hex with 0x prefix"),
            ChainRule(lambda x: bool(re.match(r"^0x[a-fA-F0-9]{64}$", x)), "Malformed hex string for transaction hash"),
        )

    @classmethod
    def gas_limit(cls, min_gas: int = 21000, max_gas: int = 15000000) -> "CryptoValidator":
        return cls(
            ChainRule(lambda x: isinstance(x, int), "Gas limit must be an integer"),
            ChainRule(lambda x: x >= min_gas, f"Gas limit below minimum threshold of {min_gas}"),
            ChainRule(lambda x: x <= max_gas, f"Gas limit exceeds maximum cap of {max_gas}"),
        )


validate_evm = CryptoValidator.evm_address()
validate_tx = CryptoValidator.tx_hash()
validate_gas = CryptoValidator.gas_limit()