
import functools, time, uuid, threading
from ..logging.mes_logger import get_logger
_THREAD = threading.local()
def get_correlation_id(): return getattr(_THREAD, "cid", None)
def with_correlation(cid=None):
    def deco(fn):
        @functools.wraps(fn)
        def w(*a, **kw):
            prev=getattr(_THREAD,"cid",None)
            try:
                _THREAD.cid = cid or prev or str(uuid.uuid4())
                return fn(*a, **kw)
            finally:
                _THREAD.cid = prev
        return w
    return deco
def traced(name=None):
    log = get_logger(name or "trace")
    def deco(fn):
        @functools.wraps(fn)
        def w(*a, **kw):
            t0=time.time(); cid=get_correlation_id() or str(uuid.uuid4())
            log.debug("start", extra={"cid": cid, "func": fn.__name__})
            try:
                r=fn(*a, **kw)
                log.info("ok", extra={"cid": cid, "func": fn.__name__, "ms": round((time.time()-t0)*1000,2)})
                return r
            except Exception:
                log.exception("fail", extra={"cid": cid, "func": fn.__name__})
                raise
        return w
    return deco
