from adapters.cache import IgniteAdapter as ignite
from common.cache import CacheManager as local

def get_cache():
    cache = ignite.get("material")
    return cache if cache else local

def get(key):
    return get_cache().get("material", key)

def put(key, value, ttl_seconds=600):
    return get_cache().put("material", key, value, ttl_seconds)

def invalidate(key=None):
    return get_cache().invalidate("material", key)
