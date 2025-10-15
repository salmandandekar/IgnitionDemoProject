from functools import wraps

from common.logging import LogFactory as LogFactory
from common.logging import LogFormatter as fmt
from common.exceptions import MESException as core

def guarded(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        log = LogFactory.get_logger("Errors")
        func_name = getattr(func, "__name__", "unknown")
        try:
            return func(*args, **kwargs)
        except core.MESException as ex:
            log.error(
                fmt.fmt(
                    "MESException",
                    code=ex.code,
                    message="{}: {}".format(func_name, ex)
                )
            )
            raise
        except Exception as ex:
            log.error(
                fmt.fmt(
                    "UnhandledException",
                    message="{} failed: {}".format(func_name, ex)
                )
            )
            raise core.MESException(
                message="Error in {}: {}".format(func_name, ex),
                user_message="An unexpected error occurred. Please contact support.",
                code="UNHANDLED",
                data={"inner": str(ex)}
            )

    return wrapper
