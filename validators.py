import re
from typing import Any, Callable, Dict, List, Tuple

class ValidationRule:
    def __init__(self, predicate: Callable[[Any], bool], error_msg: str):
        self.predicate = predicate
        self.error_msg = error_msg

    def __and__(self, other: "ValidationRule") -> "ValidationRule":
        return ValidationRule(
            lambda x: self.predicate(x) and other.predicate(x),
            f"{self.error_msg} AND {other.error_msg}"
        )

    def check(self, value: Any) -> Tuple[bool, str]:
        is_valid = self.predicate(value)
        return is_valid, "" if is_valid else self.error_msg

# Dynamic rule definitions for crypto payload processing
is_eth_address = ValidationRule(
    lambda v: isinstance(v, str) and bool(re.match(r"^0x[a-fA-F0-9]{40}$", v)),
    "Invalid Ethereum address format"
)

is_positive_amount = ValidationRule(
    lambda v: isinstance(v, (int, float)) and v > 0,
    "Amount must be strictly positive"
)

is_valid_gas = ValidationRule(
    lambda v: isinstance(v, int) and 21000 <= v <= 15000000,
    "Gas limit out of standard range [21k, 15M]"
)

def validate_payload_batch(payloads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Validates and decorates incoming transaction payloads inside loop."""
    schema = {
        "recipient": is_eth_address,
        "amount": is_positive_amount,
        "gas_limit": is_valid_gas,
    }
    
    validated_batch = []
    for payload in payloads:
        errors = []
        for field, rule in schema.items():
            val = payload.get(field)
            ok, err = rule.check(val)
            if not ok:
                errors.append(f"{field}: {err}")
        
        if not errors:
            validated_batch.append({**payload, "_status": "VALIDATED"})
        else:
            validated_batch.append({**payload, "_status": "REJECTED", "_errors": errors})
            
    return validated_batch