# Local in-memory cache with TTL support; used if Ignite is not available.
import time

_caches = {}  # {cache_name: {key: (value, expiry)}}

def _now():
    return int(time.time())

def _bucket(name):
    return _caches.setdefault(name, {})

def put(name, key, value, ttl_seconds=600):
    bucket = _bucket(name)
    expiry = _now() + ttl_seconds if ttl_seconds else None
    bucket[key] = (value, expiry)
    return True

def get(name, key):
    bucket = _bucket(name)
    if key not in bucket:
        return None
    value, expiry = bucket[key]
    if expiry and _now() > expiry:
        try:
            del bucket[key]
        except Exception:
            pass
        return None
    return value

def exists(name, key):
    return get(name, key) is not None

def invalidate(name, key=None):
    bucket = _bucket(name)
    if key is None:
        bucket.clear()
    else:
        try:
            del bucket[key]
        except Exception:
            pass
    return True
