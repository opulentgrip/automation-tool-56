import logging
import os
from logging.handlers import RotatingFileHandler

def get_crypto_logger(name='automation-tool-56', log_file='logs/app.log'):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] >> %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console output for real-time monitoring
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Rotating file handler (5MB per file, 3 backups)
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=5*1024*1024, 
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

logger = get_crypto_logger()