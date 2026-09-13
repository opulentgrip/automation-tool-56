import hashlib
import os
import logging
from logging.handlers import RotatingFileHandler

class CryptoChainRotatingHandler(RotatingFileHandler):
    """
    Rotating file handler that seals rotated log segments with a SHA-256 hash
    to verify chain-of-custody integrity.
    """
    def __init__(self, filename, maxBytes=1024*1024, backupCount=5, encoding=None, delay=False):
        super().__init__(filename, maxBytes=maxBytes, backupCount=backupCount, encoding=encoding, delay=delay)
        self.last_hash = "0" * 64

    def doRollover(self):
        super().doRollover()
        rotated_file = f"{self.baseFilename}.1"
        if os.path.exists(rotated_file):
            sha256 = hashlib.sha256()
            with open(rotated_file, "rb") as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
            self.last_hash = sha256.hexdigest()
            if self.stream:
                self.stream.write(f"\n[SYSTEM-CHAIN] BLOCK ROTATED | SEAL HASH: {self.last_hash}\n\n")
                self.flush()

def setup_crypto_logger(name: str = "crypto_automation", log_file: str = "app.log") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if logger.handlers:
        return logger

    file_handler = CryptoChainRotatingHandler(log_file, maxBytes=50000, backupCount=3, encoding="utf-8")
    
    class CryptoFormatter(logging.Formatter):
        EMOJIS = {
            logging.DEBUG: "🔍",
            logging.INFO: "⚡",
            logging.WARNING: "⚠️",
            logging.ERROR: "🚨",
            logging.CRITICAL: "💥"
        }
        def format(self, record):
            emoji = self.EMOJIS.get(record.levelno, "📝")
            original_msg = record.msg
            record.msg = f"{emoji} {original_msg}"
            result = super().format(record)
            record.msg = original_msg
            return result

    formatter = CryptoFormatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger