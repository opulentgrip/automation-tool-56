import functools
import collections
import time

CACHE_SIZE = 1024
EXPIRY_SECONDS = 30

def fast_memoize(func):
    cache = {}
    expiry = {}

    @functools.wraps(func)
    def wrapper(*args):
        now = time.time()
        if args in cache and (now - expiry.get(args, 0)) < EXPIRY_SECONDS:
            return cache[args]
        
        result = func(*args)
        cache[args] = result
        expiry[args] = now
        
        if len(cache) > CACHE_SIZE:
            oldest = next(iter(cache))
            del cache[oldest]
            del expiry[oldest]
        return result
    return wrapper

def bulk_process_tickers(data: list, func) -> list:
    # Using list comprehension for speed optimization on massive crypto payloads
    # avoids overhead of explicit loops for tick transformations
    return [func(item) for item in data if item is not None]

def dict_to_slots(cls):
    # Inject slots to reduce memory footprint per object for large ticker sets
    if '__slots__' not in cls.__dict__:
        cls.__slots__ = [attr for attr in cls.__dict__.keys() if not attr.startswith('__')]
    return cls