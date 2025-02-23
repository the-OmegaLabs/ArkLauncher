import time
import olog
from functools import wraps

def perf_monitor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        olog.output(f'{func.__name__} executed in {elapsed:.4f} seconds',
            type=olog.Type.PERF)
        return result
    return wrapper