import sys
import time
import json
import hashlib
from typing import Dict, Any

class CryptoLogChain:
    """A lightweight tamper-evident log pipeline for crypto execution trails."""
    
    LEVEL_EMOJIS = {
        "INFO": "⚡",
        "TRADE": "💎",
        "WARN": "⚠️",
        "ERROR": "🚨",
        "BULL": "📈",
        "BEAR": "📉"
    }

    def __init__(self, service_name: str = "automation-tool-56"):
        self.service = service_name
        self.last_hash = "0" * 64
        self.sequence = 0

    def _compute_hash(self, payload: Dict[str, Any]) -> str:
        serialized = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(serialized + self.last_hash.encode("utf-8")).hexdigest()

    def log(self, level: str, event: str, **kwargs: Any) -> Dict[str, Any]:
        self.sequence += 1
        timestamp = time.time_ns()
        emoji = self.LEVEL_EMOJIS.get(level.upper(), "🔍")
        
        entry = {
            "seq": self.sequence,
            "ts": timestamp,
            "service": self.service,
            "level": level.upper(),
            "event": event,
            "data": kwargs,
            "prev_hash": self.last_hash
        }
        
        curr_hash = self._compute_hash(entry)
        entry["hash"] = curr_hash
        self.last_hash = curr_hash

        formatted = f"{emoji} [{entry['level']}] #{self.sequence} | {event} | hash:{curr_hash[:8]}"
        if kwargs:
            formatted += f" | {kwargs}"
        
        sys.stdout.write(formatted + "\n")
        sys.stdout.flush()
        return entry

execution_logger = CryptoLogChain()