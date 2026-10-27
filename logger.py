import logging
import sys
from typing import Any, Optional

class CryptoLogger:
    """Custom logger for automation-tool-56 crypto operations."""

    def __init__(self, name: str = "crypto_bot") -> None:
        self._logger: logging.Logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)
        self._setup_stream()

    def _setup_stream(self) -> None:
        """Configure stream handler with cryptic formatting."""
        handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
        formatter: logging.Formatter = logging.Formatter(
            "[%(asctime)s] | %(levelname)s | ₿ %(message)s"
        )
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    def log_trade(self, symbol: str, amount: float, price: float) -> None:
        """Record execution details for a crypto transaction."""
        self._logger.info(f"EXECUTED: {symbol} @ {price} | VOL: {amount}")

    def alert(self, event: str, metadata: Optional[dict[str, Any]] = None) -> None:
        """Log critical volatility alerts with context."""
        msg: str = f"ALERT: {event} | DATA: {metadata}"
        self._logger.warning(msg)

    def debug_data(self, payload: Any) -> None:
        """Output raw API response frames."""
        self._logger.debug(f"RAW_FRAME: {payload}")