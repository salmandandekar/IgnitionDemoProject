from functools import wraps

from common.logging.LogFactory import code as LogFactory
from common.logging.LogFormatter import code as fmt
from common.exceptions.MESException import code as core

def guarded(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        log = LogFactory.get_logger("Errors")
        try:
            return func(*args, **kwargs)
        except core.MESException as ex:
            log.error(fmt.fmt("MESException", code=ex.code, message=str(ex)))
            raise
        except Exception as ex:
            log.error(
                fmt.fmt(
                    "UnhandledException",
                    type=ex.__class__.__name__,
                    message=str(ex)
                )
            )
            raise core.MESException(
                "Unhandled exception",
                code="UNHANDLED",
                data={
                    "inner": str(ex),
                    "type": ex.__class__.__name__
                }
            )
    return wrapper
