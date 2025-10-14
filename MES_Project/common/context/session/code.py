
import threading, contextlib
_ctx=threading.local()
def set_context(tenant=None, site=None, user=None):
    _ctx.tenant,_ctx.site,_ctx.user = tenant,site,user
def get_context(): return getattr(_ctx,"tenant",None), getattr(_ctx,"site",None), getattr(_ctx,"user",None)
class _NoopTM(contextlib.AbstractContextManager):
    def __enter__(self): return self
    def __exit__(self, *a): return False
def set_transaction_manager(tm): _ctx.tm=tm
def get_transaction_manager(): return getattr(_ctx,"tm", None)
def default_transaction_manager(): return _NoopTM()
