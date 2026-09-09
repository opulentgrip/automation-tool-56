from typing import Any, Dict, Optional


class CryptoAutomationError(Exception):
    """Base exception for all esoteric failures in the crypto automation tool.

    Allows injection of dynamic context payloads for remote telemetry and
    diagnostic pipeline post-mortems.
    """

    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.context: Dict[str, Any] = context or {}

    def diagnose(self) -> str:
        """Generates a unified diagnostic report combining message and metadata."""
        context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
        return f"[{self.__class__.__name__}] {self.args[0]} | Context: {{{context_str}}}"


class SlippageExceededError(CryptoAutomationError):
    """Raised when on-chain swap slippage breaches maximum tolerance threshold."""

    def __init__(
        self,
        message: str,
        expected_price: float,
        actual_price: float,
        allowed_slippage: float,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        payload = {
            "expected_price": expected_price,
            "actual_price": actual_price,
            "allowed_slippage": allowed_slippage,
        }
        if context:
            payload.update(context)
        super().__init__(message, context=payload)

    @property
    def deviation_percentage(self) -> float:
        """Calculates how much the actual price deviated from the expected price."""
        expected: float = self.context.get("expected_price", 0.0)
        actual: float = self.context.get("actual_price", 0.0)
        if expected == 0.0:
            return 0.0
        return abs((actual - expected) / expected) * 100.0


class InsufficientGasError(CryptoAutomationError):
    """Raised when the wallet lacks native gas token to execute the transaction."""

    def __init__(
        self,
        message: str,
        required_wei: int,
        available_wei: int,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        payload = {
            "required_wei": required_wei,
            "available_wei": available_wei,
        }
        if context:
            payload.update(context)
        super().__init__(message, context=payload)

    @property
    def deficit_wei(self) -> int:
        """Calculates the exact missing WEI needed to execute the transaction."""
        required = int(self.context.get("required_wei", 0))
        available = int(self.context.get("available_wei", 0))
        return max(0, required - available)
