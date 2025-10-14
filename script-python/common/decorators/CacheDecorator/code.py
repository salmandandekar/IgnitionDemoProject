from common.cache.CacheManager import code as CacheManager
from common.logging.LogFactory import code as LogFactory

def cacheable(cache_name, key_fn):
    def decorator(func):
        def wrapper(*args, **kwargs):
            log = LogFactory.get_logger("Cache")
            key = key_fn(*args, **kwargs)
            if CacheManager.exists(cache_name, key):
                log.debug("CACHE HIT: %s:%s" % (cache_name, key))
                return CacheManager.get(cache_name, key)
            res = func(*args, **kwargs)
            CacheManager.put(cache_name, key, res)
            log.debug("CACHE PUT: %s:%s" % (cache_name, key))
            return res
        return wrapper
    return decorator
