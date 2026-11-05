import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import re


class CryptoLogFormatter(logging.Formatter):
    """Custom formatter that redacts sensitive hex keys and decorates log levels."""

    KEY_REGEX = re.compile(r"\b(0x)?[a-fA-F0-9]{64}\b")

    ICONS = {
        logging.DEBUG: "🔍 [DBG]",
        logging.INFO: "⚡ [INF]",
        logging.WARNING: "⚠️  [WRN]",
        logging.ERROR: "🚨 [ERR]",
        logging.CRITICAL: "💥 [CRT]",
    }

    def format(self, record: logging.LogRecord) -> str:
        icon = self.ICONS.get(record.levelno, "[LOG]")
        original_msg = super().format(record)
        sanitized_msg = self.KEY_REGEX.sub("[REDACTED_KEY]", original_msg)
        return f"{icon} {sanitized_msg}"


def get_crypto_logger(
    name: str = "crypto_automation",
    log_dir: str = "logs",
    max_mb: int = 5,
    backups: int = 3,
) -> logging.Logger:
    path = Path(log_dir)
    path.mkdir(parents=True, exist_ok=True)
    log_file = path / f"{name}.log"

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_mb * 1024 * 1024,
        backupCount=backups,
        encoding="utf-8",
    )
    file_fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )
    file_handler.setFormatter(file_fmt)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        CryptoLogFormatter("%(asctime)s | %(message)s", datefmt="%H:%M:%S")
    )

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
