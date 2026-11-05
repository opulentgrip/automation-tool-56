import sys
import time
from typing import Any, Dict, Literal, Optional, TextIO

LogLevel = Literal["INFO", "WARN", "SELL", "BUY", "REBAL"]


class CryptoStreamLogger:
    """A high-frequency telemetry logger tailored for crypto automation feeds.

    Injects market indicators, timestamp offsets, and directional unicode glyphs
    into stdout/stderr or custom IO streams.
    """

    GLYPHS: Dict[LogLevel, str] = {
        "INFO": "⚡",
        "WARN": "⚠️",
        "SELL": "🔴",
        "BUY": "🟢",
        "REBAL": "🔄",
    }

    def __init__(
        self, stream: TextIO = sys.stdout, include_epoch: bool = True
    ) -> None:
        self.stream: TextIO = stream
        self.include_epoch: bool = include_epoch
        self._counter: int = 0

    def emit(
        self, level: LogLevel, event: str, metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Formats and prints a ledger-style telemetry entry to the configured stream.

        Args:
            level: Categorical priority/action identifier for the log.
            event: Short descriptive message of the crypto event.
            metadata: Additional key-value pairs representing prices, gas, or tx hashes.

        Returns:
            The raw formatted line emitted to the stream.
        """
        self._counter += 1
        ts: str = f"[{int(time.time())}] " if self.include_epoch else ""
        glyph: str = self.GLYPHS.get(level, "💬")

        meta_str: str = ""
        if metadata:
            items = [f"{k}={v}" for k, v in metadata.items()]
            meta_str = f" | {', '.join(items)}"

        formatted: str = f"{ts}{glyph} #{self._counter:05d} [{level}] {event}{meta_str}\n"
        self.stream.write(formatted)
        self.stream.flush()
        return formatted.strip()


def get_crypto_logger(
    stderr_fallback: bool = False,
) -> CryptoStreamLogger:
    """Factory function producing an initialized CryptoStreamLogger instance.

    Args:
        stderr_fallback: If True, channels stream output directly to sys.stderr.

    Returns:
        A ready-to-use CryptoStreamLogger instance.
    """
    target_stream = sys.stderr if stderr_fallback else sys.stdout
    return CryptoStreamLogger(stream=target_stream)
