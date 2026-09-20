import logging
import json
from datetime import datetime

class CryptoTransactionHandler:
    def __init__(self, storage_path='tx_cache.log'):
        self.storage = storage_path
        self.logger = logging.getLogger('automation-tool-56')

    def sanitize(self, raw_data):
        return {k: v for k, v in raw_data.items() if v is not None}

    def process_queue(self, transactions):
        processed = []
        for tx in transactions:
            try:
                clean_tx = self.sanitize(tx)
                clean_tx['timestamp'] = datetime.utcnow().isoformat()
                processed.append(clean_tx)
            except Exception as e:
                self.logger.error(f'transaction parsing failure: {e}')
        return processed

    def flush_to_disk(self, data):
        with open(self.storage, 'a') as f:
            for entry in data:
                f.write(json.dumps(entry) + '\n')

    def execute(self, payload):
        if not payload:
            return False
        batch = self.process_queue(payload)
        self.flush_to_disk(batch)
        return True