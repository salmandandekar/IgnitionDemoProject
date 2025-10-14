
import functools
from ..context.session import get_transaction_manager
def transactional(fn):
    @functools.wraps(fn)
    def w(*a, **kw):
        tm = get_transaction_manager()
        if tm is None: return fn(*a, **kw)
        with tm: return fn(*a, **kw)
    return w
