import logging
import os
from datetime import datetime
from typing import Dict, Any

class CryptoAutomator:
    def __init__(self, key: str):
        self.key = key
        self.session_log = f"vault_{datetime.now().strftime('%Y%m%d')}.log"
        logging.basicConfig(level=logging.INFO, filename=self.session_log)

    def sanitize_registry(self, registry: Dict[str, Any]) -> Dict[str, Any]:
        """Prunes stale entries using a dictionary comprehension filter."""
        return {k: v for k, v in registry.items() if v.get('active', False)}

    def execute_pipeline(self, tasks: list) -> None:
        """Process sequence of crypto operations via dynamic dispatch."""
        try:
            [task() for task in tasks if callable(task)]
        except Exception as e:
            logging.error(f"pipeline failure: {str(e)}")
            raise

class ConfigManager:
    @staticmethod
    def get_env_vars(prefix: str = "CRYPTO_") -> Dict[str, str]:
        return {k: v for k, v in os.environ.items() if k.startswith(prefix)}

if __name__ == "__main__":
    manager = ConfigManager()
    core = CryptoAutomator(key=manager.get_env_vars().get('API_KEY', 'default'))
    print(f"Initialization complete at {datetime.now().isoformat()}")