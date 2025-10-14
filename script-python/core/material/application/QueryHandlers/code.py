from common.decorators.TraceDecorator import code as tracedec
from common.decorators.ExceptionHandlerDecorator import code as exdec
from common.decorators.CacheDecorator import code as cdec
from adapters.cache.IgniteAdapter import code as ignite
from common.logging.LogFactory import code as LogFactory

def _cache_key(q): 
    return "material:%s" % q.id

@tracedec.traced
@exdec.guarded
@cdec.cacheable(cache_name="material", key_fn=lambda q: _cache_key(q))
def handle_get_by_id(q, repository):
    # cache decorator will store result using key; repository will only hit DB if not in cache
    return repository.get_by_id(q.id)
