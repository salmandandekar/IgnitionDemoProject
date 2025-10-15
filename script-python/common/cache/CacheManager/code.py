# Local in-memory cache with TTL support; used if Ignite is not available.
import time

_caches = {}  # {cache_name: {key: (value, expiry, ttl)}}
_SENTINEL = object()


def _now():
    return int(time.time())


def _bucket(name):
    return _caches.setdefault(name, {})


def _wrap_value(value):
    if value is None:
        return _SENTINEL
    return value


def _unwrap_value(stored):
    if stored is _SENTINEL:
        return None
    return stored


def _normalized_ttl(ttl_seconds):
    if ttl_seconds is None:
        return None
    try:
        ttl_value = int(ttl_seconds)
    except Exception:
        try:
            ttl_value = int(float(ttl_seconds))
        except Exception:
            ttl_value = 0
    if ttl_value <= 0:
        return None
    return ttl_value


def _get_entry(name, key):
    bucket = _bucket(name)
    entry = bucket.get(key)
    if entry is None:
        return None

    entry_len = 0
    if isinstance(entry, tuple):
        entry_len = len(entry)
        if entry_len >= 3:
            stored, expiry, ttl_value = entry[0], entry[1], entry[2]
        elif entry_len == 2:
            stored, expiry = entry
            ttl_value = None
        else:
            stored = entry[0]
            expiry = None
            ttl_value = None
    else:
        stored = entry
        expiry = None
        ttl_value = None

    current = _now()
    if expiry is not None and current > expiry:
        try:
            del bucket[key]
        except Exception:
            pass
        return None

    if entry_len != 3:
        stored = _wrap_value(_unwrap_value(stored))
        bucket[key] = (stored, expiry, ttl_value)

    return stored, expiry, ttl_value


def put(name, key, value, ttl_seconds=600):
    bucket = _bucket(name)
    ttl_value = _normalized_ttl(ttl_seconds)
    expiry = _now() + ttl_value if ttl_value is not None else None
    bucket[key] = (_wrap_value(value), expiry, ttl_value)
    return True


def get(name, key):
    entry = _get_entry(name, key)
    if entry is None:
        return None
    stored, _, _ = entry
    return _unwrap_value(stored)


def exists(name, key):
    return _get_entry(name, key) is not None


def get_ttl(name, key):
    entry = _get_entry(name, key)
    if entry is None:
        return None
    _, expiry, ttl_value = entry
    if ttl_value is not None:
        return ttl_value
    if expiry is None:
        return None
    remaining = expiry - _now()
    if remaining <= 0:
        return 0
    return remaining


def invalidate(name, key=None):
    bucket = _bucket(name)
    if key is None:
        bucket.clear()
    else:
        if key in bucket:
            try:
                del bucket[key]
            except Exception:
                pass
    return True
