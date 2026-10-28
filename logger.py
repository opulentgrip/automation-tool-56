import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import re
import sys


class CryptoSymbolFormatter(logging.Formatter):
    """Custom formatter highlighting crypto symbols and transaction hashes."""

    TICKER_PATTERN = re.compile(r"\b(BTC|ETH|SOL|USDT|BNB|XRP|ADA|DOGE)\b")
    HEX_PATTERN = re.compile(r"\b0x[a-fA-F0-9]{40}\b")

    def __init__(self, fmt=None, datefmt=None, colorize=True):
        super().__init__(fmt, datefmt)
        self.colorize = colorize

    def format(self, record):
        message = super().format(record)
        if self.colorize:
            message = self.TICKER_PATTERN.sub(r"[⚡\1]", message)
            message = self.HEX_PATTERN.sub(
                lambda m: f"🔗{m.group(0)[:6]}...{m.group(0)[-4:]}", message
            )
        return message


def get_crypto_logger(
    name: str = "crypto_auto",
    log_file: str = "bot_activity.log",
    max_bytes: int = 2 * 1024 * 1024,
    backup_count: int = 5,
) -> logging.Logger:
    """Configures and returns a dual console/rotating-file logger."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    log_path = Path("logs")
    log_path.mkdir(exist_ok=True)
    full_path = log_path / log_file

    log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(
        CryptoSymbolFormatter(log_format, date_format, colorize=True)
    )

    file_handler = RotatingFileHandler(
        full_path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        CryptoSymbolFormatter(log_format, date_format, colorize=False)
    )

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


bot_logger = get_crypto_logger()
