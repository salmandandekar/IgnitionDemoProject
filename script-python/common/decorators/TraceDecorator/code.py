from functools import wraps

from common.logging import LogFactory as LogFactory
from common.logging import LogFormatter as fmt
from common.context import SessionContext as Session


def traced(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        log = LogFactory.get_logger("Trace")
        ctx = Session.current()
        correlation_id = ctx.get("correlationId")
        log.debug(
            fmt.fmt(
                "ENTER",
                function=func.__name__,
                correlationId=correlation_id
            )
        )
        status = "OK"
        try:
            result = func(*args, **kwargs)
            return result
        except Exception:
            status = "ERROR"
            raise
        finally:
            log.debug(
                fmt.fmt(
                    "EXIT",
                    function=func.__name__,
                    correlationId=correlation_id,
                    status=status
                )
            )
    return wrapper
