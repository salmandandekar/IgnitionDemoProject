from functools import wraps


# Simple transaction wrapper for write operations

def transactional(datasource):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tx = None
            begin = commit = rollback = close = None
            try:
                try:
                    from system.db import beginTransaction as begin
                    from system.db import commitTransaction as commit
                    from system.db import rollbackTransaction as rollback
                    from system.db import closeTransaction as close
                except Exception:
                    # outside Ignition, no-op
                    return func(*args, **kwargs)
                if "_tx" in kwargs and kwargs.get("_tx") is not None:
                    return func(*args, **kwargs)
                tx = begin(datasource)
                if "_tx" not in kwargs:
                    kwargs["_tx"] = tx
                res = func(*args, **kwargs)
                commit(tx)
                return res
            except Exception:
                if tx is not None and rollback is not None:
                    try:
                        rollback(tx)
                    except Exception:
                        pass
                raise
            finally:
                if tx is not None and close is not None:
                    try:
                        close(tx)
                    except Exception:
                        pass
        return wrapper

    return decorator
