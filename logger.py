import logging
import os
from logging.handlers import RotatingFileHandler

def get_crypto_logger(name='automation-tool-56', log_file='crypto_engine.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        # Creative formatter for crypto-specific telemetry
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | [TX-MONITOR] | %(message)s'
        )
        
        # Rolling log files capped at 5MB, keep 3 historical versions
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=5 * 1024 * 1024, 
            backupCount=3
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Stream logs to stdout for real-time visibility
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
    
    return logger

# Instantiate the logger as a module singleton for easy access
crypto_logger = get_crypto_logger()