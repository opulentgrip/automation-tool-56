import logging
import sys
from typing import Any, Optional

class CryptoLogger:
    """
    A vibrant logger for the automation-tool-56 environment.
    Uses standard logging but with a splash of blockchain-themed formatting.
    """
    def __init__(self, name: str = "crypto_bot") -> None:
        self.logger: logging.Logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
        formatter: logging.Formatter = logging.Formatter(
            "[%(asctime)s] | %(levelname)s | %(name)s >>> %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_trade(self, pair: str, side: str, price: float, amount: float) -> None:
        """
        Logs trade execution events with structured data for audit trails.
        """
        msg: str = f"TRADE_EXEC: {side.upper()} {amount} {pair} @ {price}"
        self.logger.info(msg)

    def warn_risk(self, alert_type: str, details: Optional[Any] = None) -> None:
        """
        Emits a warning when risk parameters are breached.
        """
        self.logger.warning(f"RISK_ALERT: {alert_type} | Details: {details or 'none'}")

    def fatal_exit(self, error: Exception) -> None:
        """
        Critical failure logger for abrupt halt routines.
        """
        self.logger.critical(f"SYSTEM_HALT: {type(error).__name__} occurred. Shutdown initiated.")