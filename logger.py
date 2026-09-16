import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path

class CryptoLogger:
    def __init__(self, name='crypto_node', log_dir='logs', max_bytes=5*1024*1024, backup_count=3):
        self.log_path = Path(log_dir)
        self.log_path.mkdir(exist_ok=True)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # using a custom formatter with hex-like aesthetics for blockchain tracking
        formatter = logging.Formatter(
            '[%(asctime)s] 0x%(levelname)s - %(name)s::%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # rotating handler for high frequency crypto-log volume
        handler = RotatingFileHandler(
            self.log_path / f'{name}.log',
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # console fallback
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self.logger.addHandler(console)

    def get_logger(self):
        return self.logger

# setup instance for automation-tool-56 usage
logger = CryptoLogger().get_logger()