import logging
from typing import Dict, Any, Callable

class CryptoPayloadValidator:
    def __init__(self, schema: Dict[str, type]):
        self.schema = schema

    def __call__(self, data: Dict[str, Any]) -> bool:
        return all(isinstance(data.get(k), v) for k, v in self.schema.items())

def process_trade(payload: Dict[str, Any]) -> None:
    print(f"Executing {payload.get('pair')} trade at {payload.get('price')}")

def main_loop(queue: list, validator: CryptoPayloadValidator) -> None:
    while queue:
        packet = queue.pop(0)
        try:
            if not validator(packet):
                raise ValueError(f"Invalid packet schema: {packet}")
            process_trade(packet)
        except (ValueError, KeyError) as e:
            logging.error(f"Corruption in stream: {e}")
            continue

if __name__ == '__main__':
    crypto_schema = {'pair': str, 'price': float, 'volume': int}
    validator = CryptoPayloadValidator(crypto_schema)
    mock_queue = [
        {'pair': 'BTC/USDT', 'price': 65000.5, 'volume': 1},
        {'pair': 'ETH/USDT', 'price': 'invalid', 'volume': 10},
        {'pair': 'SOL/USDT', 'price': 140.2, 'volume': 5}
    ]
    main_loop(mock_queue, validator)