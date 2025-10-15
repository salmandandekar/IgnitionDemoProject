from common.cache import IgniteCacheProvider as ignite
from common.cache import CacheManager as local

def get(cache_name):
    # Try Ignite; fallback to local cache bucket (managed by CacheManager)
    if ignite.available():
        return ignite.get(cache_name)
    return local  # return module providing get/put/exists/invalidate
