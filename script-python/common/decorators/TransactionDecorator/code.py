# Simple transaction wrapper for write operations
def transactional(datasource):
    def decorator(func):
        def wrapper(*args, **kwargs):
            tx = None
            try:
                try:
                    from system.db import beginTransaction, commitTransaction, rollbackTransaction, closeTransaction
                except Exception:
                    # outside Ignition, no-op
                    return func(*args, **kwargs)
                tx = beginTransaction(datasource)
                kwargs["_tx"] = tx
                res = func(*args, **kwargs)
                commitTransaction(tx) 
                return res
            except Exception:
                if tx is not None:
                    try:
                        rollbackTransaction(tx)
                    except Exception:
                        pass
                raise
            finally:
                if tx is not None:
                    try:
                        from system.db import closeTransaction
                        closeTransaction(tx)
                    except Exception:
                        pass
        return wrapper
    return decorator
