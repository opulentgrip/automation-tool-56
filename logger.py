import logging
import sys
from datetime import datetime

class CryptoFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',
        'INFO': '\033[92m',
        'WARNING': '\033[93m',
        'ERROR': '\033[91m',
        'CRITICAL': '\033[41m\033[97m'
    }
    
    def format(self, record):
        log_fmt = f"{self.COLORS.get(record.levelname, '')}[%(asctime)s] | %(levelname)s | %(message)s\033[0m"
        formatter = logging.Formatter(log_fmt, datefmt='%H:%M:%S')
        return formatter.format(record)

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(CryptoFormatter())
        logger.addHandler(handler)
    
    return logger

def audit_log(event: str, data: dict):
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    with open('automation-tool-56.log', 'a') as f:
        f.write(f"{timestamp} | {event} | {data}\n")