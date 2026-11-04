import logging
import sys
from typing import Any, Optional

class CryptoLogger:
    """Custom logger for automation-tool-56 crypto operations."""

    def __init__(self, name: str = "crypto_bot") -> None:
        self._logger: logging.Logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)
        handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
        formatter: logging.Formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    def log_trade(self, symbol: str, amount: float, price: float) -> None:
        """Formats and outputs trade execution details to stdout."""
        self._logger.info(f"EXECUTE: {symbol} @ {price} | Vol: {amount}")

    def alert_anomaly(self, msg: str, code: Optional[int] = None) -> None:
        """Dispatches critical crypto price anomaly warnings."""
        tag: str = f"[CODE:{code}]" if code else ""
        self._logger.warning(f"ANOMALY DETECTED {tag}: {msg}")

    def __call__(self, msg: Any) -> None:
        """Syntactic sugar for quick diagnostic logging."""
        self._logger.debug(f"DEBUG: {str(msg)}")

logger: CryptoLogger = CryptoLogger()