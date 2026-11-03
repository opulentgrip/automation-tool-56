import logging
from logging.handlers import RotatingFileHandler
import sys
import os

class CryptoLogger:
    def __init__(self, name='automation-tool-56', log_file='crypto_ops.log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | [%(process)d] | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        file_path = os.path.join('logs', log_file)
        file_handler = RotatingFileHandler(
            file_path, 
            maxBytes=5*1024*1024, 
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger

log = CryptoLogger().get_logger()