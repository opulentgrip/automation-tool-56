import os
import logging
from logging.handlers import RotatingFileHandler

CRYPTO_LOG_FORMAT = '%(asctime)s | ₿ | %(levelname)s | [%(filename)s:%(lineno)d] - %(message)s'

def setup_crypto_logger(name: str = 'automation_tool_56', log_file: str = 'crypto_ops.log') -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
        
    logger.setLevel(logging.DEBUG)
    
    os.makedirs(os.path.dirname(log_file) if os.path.dirname(log_file) else '.', exist_ok=True)
    
    file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(CRYPTO_LOG_FORMAT)
    file_handler.setFormatter(file_formatter)
    
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_formatter = logging.Formatter(CRYPTO_LOG_FORMAT)
    stream_handler.setFormatter(stream_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    
    return logger

logger = setup_crypto_logger()
