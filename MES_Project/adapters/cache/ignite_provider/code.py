
from ...common.cache.cache_provider import CacheProvider
from ...common.logging.mes_logger import get_logger
log=get_logger("IgniteCache")
class IgniteCacheProvider(CacheProvider):
    def __init__(self): self._mem={}
    def get(self, region, key): return self._mem.get(region, {}).get(key)
    def set(self, region, key, value, ttl=None):
        self._mem.setdefault(region, {})[key]=value; log.info("set", extra={"region": region}); return True
