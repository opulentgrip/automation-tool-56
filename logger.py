import logging
import sys
from typing import Any, Final

class CryptoLogger:
    """Custom logger for automation-tool-56 crypto operations."""

    FORMAT: Final[str] = "%(asctime)s | %(levelname)-8s | %(message)s"

    def __init__(self, name: str = "crypto_bot") -> None:
        self._logger: logging.Logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)
        handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(self.FORMAT))
        self._logger.addHandler(handler)

    def log_trade(self, symbol: str, amount: float, price: float) -> None:
        """Record trade execution events to standard output."""
        msg: str = f"TRADE EXECUTION: {symbol} | QTY: {amount} | PRICE: ${price:.2f}"
        self._logger.info(msg)

    def log_alert(self, severity: str, message: Any) -> None:
        """Categorize high-priority crypto events based on severity."""
        payload: str = f"[ALERT-{severity.upper()}] {message}"
        if severity == "critical":
            self._logger.critical(payload)
        else:
            self._logger.warning(payload)

    def log_debug(self, data: dict[str, Any]) -> None:
        """Format dictionary snapshots for debugging state transitions."""
        pretty: str = " | ".join(f"{k.upper()}={v}" for k, v in data.items())
        self._logger.debug(f"STATE SNAPSHOT: {pretty}")