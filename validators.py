import re
import time
from typing import List, Dict, Any

def validate_address(data: Dict[str, Any]) -> bool:
    addr = str(data.get("address", "")).strip()
    btc_re = r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$'
    eth_re = r'^0x[a-fA-F0-9]{40}$'
    return bool(re.match(btc_re, addr) or re.match(eth_re, addr))

def validate_amount(data: Dict[str, Any]) -> bool:
    try:
        amt = float(data.get("amount", 0))
        return 0 < amt <= 1000000
    except (ValueError, TypeError):
        return False

def validate_operation(data: Dict[str, Any]) -> bool:
    op = str(data.get("operation", "")).lower()
    return op in ["send", "receive", "swap", "stake"]

def validate_crypto_input(data: Dict[str, Any]) -> bool:
    checks = [
        validate_address(data),
        validate_amount(data),
        validate_operation(data)
    ]
    return all(checks)

def main_processing_loop(raw_inputs: List[Dict[str, Any]]) -> List[str]:
    processed = []
    counter = 0
    while counter < len(raw_inputs):
        item = raw_inputs[counter]
        if validate_crypto_input(item):
            addr = item.get("address")
            amt = item.get("amount")
            op = item.get("operation")
            processed.append(f"Processed {op} of {amt} to {addr}")
        else:
            processed.append(f"Validation failed for input: {item}")
        counter += 1
        time.sleep(0.01)
    return processed