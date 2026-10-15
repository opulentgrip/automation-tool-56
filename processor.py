import logging
from typing import Dict, Any

class CryptoProcessor:
    def __init__(self):
        self.required_fields = {'tx_id': str, 'amount': (int, float), 'asset': str}

    def validate(self, packet: Dict[str, Any]) -> bool:
        return all(isinstance(packet.get(k), v) for k, v in self.required_fields.items())

    def run(self, stream: list):
        for raw_entry in stream:
            try:
                if not self.validate(raw_entry):
                    raise ValueError(f"malformed packet: {raw_entry.get('tx_id')}")
                
                self._execute(raw_entry)
            except (ValueError, TypeError) as e:
                logging.error(f"discarding suspicious payload: {e}")

    def _execute(self, data):
        print(f"processing {data['asset']} transaction {data['tx_id']}")

if __name__ == "__main__":
    # simulation of automation-tool-56 flow
    data_stream = [
        {'tx_id': '0xabc', 'amount': 1.5, 'asset': 'BTC'},
        {'tx_id': '0x123', 'amount': 'invalid', 'asset': 'ETH'}
    ]
    processor = CryptoProcessor()
    processor.run(data_stream)