import os
import hashlib
import logging
from logging.handlers import RotatingFileHandler

class LedgerFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None):
        super().__init__(fmt, datefmt)
        self.prev_hash = "0" * 64

    def format(self, record):
        original_msg = record.getMessage()
        data_to_hash = f"{self.prev_hash}|{record.created}|{original_msg}"
        current_hash = hashlib.sha256(data_to_hash.encode('utf-8')).hexdigest()
        
        record.prev_hash = self.prev_hash[:8]
        record.curr_hash = current_hash[:8]
        self.prev_hash = current_hash
        
        return super().format(record)

def setup_logger(log_file="ledger.log", max_bytes=5 * 1024 * 1024, backup_count=5):
    logger = logging.getLogger("CryptoLedger")
    logger.setLevel(logging.DEBUG)
    
    if logger.hasHandlers():
        logger.handlers.clear()

    fmt = "[%(asctime)s] [%(levelname)s] [Prev: %(prev_hash)s] [Curr: %(curr_hash)s] %(message)s"
    formatter = LedgerFormatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")

    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
