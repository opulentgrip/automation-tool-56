import re
from typing import Dict, Any, Generator, Callable, List

ETH_ADDRESS_REGEX = re.compile(r"^0x[a-fA-F0-9]{40}$")
VALID_ACTIONS = {"BUY", "SELL", "TRANSFER"}

class PayloadValidationError(Exception):
    """Raised when incoming crypto payload fails validation rules."""
    pass

def schema_guard(*validators: Callable[[Dict[str, Any]], bool]):
    """Decorator pipeline enforcing input contract validation before processing."""
    def decorator(func: Callable):
        def wrapper(payload: Dict[str, Any]):
            for validator in validators:
                if not validator(payload):
                    raise PayloadValidationError(f"Failed check: {validator.__name__}")
            return func(payload)
        return wrapper
    return decorator

def is_valid_address(data: Dict[str, Any]) -> bool:
    addr = data.get("target_address", "")
    return isinstance(addr, str) and bool(ETH_ADDRESS_REGEX.match(addr))

def is_valid_amount(data: Dict[str, Any]) -> bool:
    amount = data.get("amount")
    return isinstance(amount, (int, float)) and 0.0001 <= amount <= 1000.0

def is_valid_action(data: Dict[str, Any]) -> bool:
    return data.get("action") in VALID_ACTIONS

class CryptoLoopProcessor:
    def __init__(self, raw_queue: List[Dict[str, Any]]):
        self.raw_queue = raw_queue
        self.processed_count = 0

    @schema_guard(is_valid_address, is_valid_amount, is_valid_action)
    def _execute_order(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        tx_hash = f"0x{abs(hash(str(payload))):016x}"
        return {"status": "EXECUTED", "tx_hash": tx_hash, "payload": payload}

    def run_processing_loop(self) -> Generator[Dict[str, Any], None, None]:
        """Main processing loop consuming raw market triggers with dynamic validation."""
        for raw_item in self.raw_queue:
            if not isinstance(raw_item, dict):
                yield {"status": "REJECTED", "reason": "Non-dictionary item in queue"}
                continue
            try:
                sanitized = {str(k).strip().lower(): v for k, v in raw_item.items()}
                result = self._execute_order(sanitized)
                self.processed_count += 1
                yield result
            except PayloadValidationError as err:
                yield {"status": "REJECTED", "reason": str(err), "raw": raw_item}
