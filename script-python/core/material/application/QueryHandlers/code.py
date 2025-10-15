from common.decorators import TraceDecorator as tracedec
from common.decorators import ExceptionHandlerDecorator as exdec
from common.decorators import CacheDecorator as cdec
from adapters.cache import IgniteAdapter as ignite
from common.logging import LogFactory as LogFactory

def _cache_key(q): 
    return "material:%s" % q.id

@tracedec.traced
@exdec.guarded
@cdec.cacheable(cache_name="material", key_fn=lambda q: _cache_key(q))
def handle_get_by_id(q, repository):
    # cache decorator will store result using key; repository will only hit DB if not in cache
    return repository.get_by_id(q.id)
