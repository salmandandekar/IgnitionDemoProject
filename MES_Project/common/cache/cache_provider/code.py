
from threading import RLock
from ..logging.mes_logger import get_logger
log=get_logger("Cache")
class CacheProvider(object):
    def get(self, region, key): raise NotImplementedError
    def set(self, region, key, value, ttl=None): raise NotImplementedError
class InMemoryCache(CacheProvider):
    def __init__(self): self._d={}; self._lock=RLock()
    def get(self, region, key):
        with self._lock: return self._d.get(region, {}).get(key)
    def set(self, region, key, value, ttl=None):
        with self._lock: self._d.setdefault(region, {})[key]=value; return True
_provider=InMemoryCache()
def use_provider(p):
    global _provider; _provider=p or _provider
    log.info("provider-set", extra={"provider": p.__class__.__name__ if p else "default"})
def get(region, key): return _provider.get(region, key)
def set(region, key, value, ttl=None): return _provider.set(region, key, value, ttl)
