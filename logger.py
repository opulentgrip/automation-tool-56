import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path('logs')
LOG_DIR.mkdir(exist_ok=True)

class CryptoFormatter(logging.Formatter):
    """Colorful and concise logs for rapid crypto trading analysis."""
    formats = {
        logging.INFO: "[%(asctime)s] 🚀 %(message)s",
        logging.ERROR: "[%(asctime)s] 💀 %(message)s",
        logging.DEBUG: "[%(asctime)s] 🔍 %(message)s"
    }

    def format(self, record):
        log_fmt = self.formats.get(record.levelno, "[%(asctime)s] ⚙️ %(message)s")
        formatter = logging.Formatter(log_fmt, datefmt="%H:%M:%S")
        return formatter.format(record)

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        file_handler = RotatingFileHandler(
            LOG_DIR / f"{name}.log", 
            maxBytes=5_000_000, 
            backupCount=3
        )
        file_handler.setFormatter(CryptoFormatter())
        logger.addHandler(file_handler)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(CryptoFormatter())
        logger.addHandler(console_handler)
        
    return logger