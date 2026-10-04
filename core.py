import random
import time
import urllib.request
import json
from typing import Dict, List, Any, Optional

class ResilientNodeRouter:
    """
    An unconventional Ethereum JSON-RPC router designed to handle edge cases
    such as dirty responses, rate limits, and flaky nodes by using a prime-modulo
    retry jitter and fallback chain selection.
    """
    def __init__(self, endpoints: List[str]):
        self.endpoints = endpoints or ["https://cloudflare-eth.com"]
        self._prime_jitters = [2, 3, 5, 7, 11, 13]

    def _calculate_delay(self, attempt: int) -> float:
        # Creative backoff: prime number modulated by a random float factor
        prime = self._prime_jitters[attempt % len(self._prime_jitters)]
        return prime * random.uniform(0.5, 1.5)

    def query_rpc(self, method: str, params: List[Any]) -> Optional[Dict[str, Any]]:
        payload = json.dumps({
            "jsonrpc": "2.0",
            "id": int(time.time() * 1000),
            "method": method,
            "params": params
        }).encode('utf-8')

        for attempt in range(len(self.endpoints) * 2):
            endpoint = self.endpoints[attempt % len(self.endpoints)]
            try:
                req = urllib.request.Request(
                    endpoint,
                    data=payload,
                    headers={
                        'Content-Type': 'application/json',
                        'User-Agent': f'CryptoChaosBuster/{attempt}'
                    }
                )
                with urllib.request.urlopen(req, timeout=4) as response:
                    raw_data = response.read()
                    # Sanitization: strip potential header overflow leakage sometimes present in raw payloads
                    start = raw_data.find(b'{')
                    end = raw_data.rfind(b'}')
                    if start == -1 or end == -1:
                        raise ValueError("Malformed non-JSON package received from peer node")
                    
                    clean_data = raw_data[start:end+1]
                    data = json.loads(clean_data.decode('utf-8'))
                    
                    if 'error' in data:
                        raise ValueError(f"Node returned custom RPC error: {data['error'].get('message')}")
                    return data.get('result')
            except Exception:
                # Catch network issues, dirty responses, or timeout constraints
                delay = self._calculate_delay(attempt)
                time.sleep(delay)
                continue
        raise RuntimeError("All configured blockchain gateway endpoints exhausted and failed to respond")