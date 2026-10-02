import hashlib
from dataclasses import dataclass, field
from typing import Callable, Generator

@dataclass
class CryptoPayload:
    tx_hash: str
    raw_hex: str
    metadata: dict = field(default_factory=dict)
    stage_history: list = field(default_factory=list)

class ProcessingPipeline:
    """Unconventional decorator-driven processing pipeline for crypto payloads."""
    def __init__(self):
        self._stages: list[tuple[str, Callable[[CryptoPayload], CryptoPayload]]] = []

    def stage(self, name: str):
        def decorator(func: Callable[[CryptoPayload], CryptoPayload]):
            self._stages.append((name, func))
            return func
        return decorator

    def __call__(self, initial_payload: CryptoPayload) -> CryptoPayload:
        current = initial_payload
        for name, func in self._stages:
            current = func(current)
            current.stage_history.append(name)
        return current

pipeline = ProcessingPipeline()

@pipeline.stage("hash_validation")
def validate_hash(payload: CryptoPayload) -> CryptoPayload:
    computed = hashlib.sha256(payload.raw_hex.encode()).hexdigest()
    payload.metadata["digest_match"] = (computed == payload.tx_hash)
    return payload

@pipeline.stage("gas_fee_projection")
def estimate_gas(payload: CryptoPayload) -> CryptoPayload:
    payload_len = len(payload.raw_hex)
    base_fee = 21000
    payload.metadata["estimated_gas"] = base_fee + (payload_len * 16)
    return payload

@pipeline.stage("mempool_tagging")
def tag_mempool(payload: CryptoPayload) -> CryptoPayload:
    is_priority = payload.metadata.get("estimated_gas", 0) > 25000
    payload.metadata["priority_flag"] = is_priority
    return payload

def process_transaction_batch(raw_transactions: list[dict]) -> Generator[CryptoPayload, None, None]:
    for tx in raw_transactions:
        payload = CryptoPayload(tx_hash=tx["hash"], raw_hex=tx["hex"])
        yield pipeline(payload)
