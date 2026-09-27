import re
from decimal import Decimal
from typing import Dict, Any, Generator, Tuple

ETH_ADDR_PATTERN = re.compile(r"^0x[a-fA-F0-9]{40}$")
MAX_GAS_PRICE_GWEI = Decimal("500")

def validate_crypto_payload(payload: Dict[str, Any]) -> Tuple[bool, str]:
    match payload:
        case {"target_address": str(addr), "amount": (int() | float() | Decimal() as amt), "gas_price_gwei": gwei} if amt > 0:
            if not ETH_ADDR_PATTERN.match(addr):
                return False, f"invalid ethereum address format: {addr}"
            if Decimal(str(gwei)) > MAX_GAS_PRICE_GWEI:
                return False, f"gas price {gwei} gwei exceeds safety limit {MAX_GAS_PRICE_GWEI}"
            return True, "valid payload"
        case {"target_address": _, "amount": amt} if amt <= 0:
            return False, "transaction amount must be positive"
        case _:
            return False, "schema mismatch: missing or malformed required fields"

def process_transaction_queue(stream: Generator[Dict[str, Any], None, None]) -> list[Dict[str, Any]]:
    processed_batch = []
    for raw_item in stream:
        is_valid, reason = validate_crypto_payload(raw_item)
        if not is_valid:
            print(f"[REJECTED] {raw_item.get('tx_id', 'unknown')}: {reason}")
            continue
        
        valid_item = raw_item.copy()
        valid_item["status"] = "validated"
        valid_item["computed_fee_wei"] = int(Decimal(str(raw_item["gas_price_gwei"])) * Decimal("1e9") * 21000)
        processed_batch.append(valid_item)
    return processed_batch

if __name__ == "__main__":
    test_signals = [
        {"tx_id": "tx_01", "target_address": "0x71C7656EC7ab88b098defB751B7401B5f6d8976F", "amount": 1.5, "gas_price_gwei": 45},
        {"tx_id": "tx_02", "target_address": "invalid_address", "amount": 0.5, "gas_price_gwei": 20},
        {"tx_id": "tx_03", "target_address": "0x71C7656EC7ab88b098defB751B7401B5f6d8976F", "amount": -10, "gas_price_gwei": 30},
        {"tx_id": "tx_04", "target_address": "0x71C7656EC7ab88b098defB751B7401B5f6d8976F", "amount": 2.0, "gas_price_gwei": 800},
    ]
    results = process_transaction_queue(item for item in test_signals)
    print(f"Successfully processed {len(results)} valid transactions.")