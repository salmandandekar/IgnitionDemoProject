import traceback
from common.logging import LogFactory
from common.logging import LogFormatter as fmt
from common.exceptions import MESException as core

def guarded(func):
    def wrapper(*args, **kwargs):
        log = LogFactory.get_logger("Errors")
        func_name = getattr(func, "__name__", "unknown")
        try:
            return func(*args, **kwargs)

        except core.MESException as ex:
            log.error(fmt.fmt(
                "MESException",
                code=ex.code,
                message="{}: {}".format(func_name, ex)
            ))
            return ex.user_message

        except Exception as ex:
            # Combine summary + traceback into one single message
            tb_str = traceback.format_exc()
            full_message = "{} failed: {}\n{}".format(func_name, ex, tb_str)
            log.error(fmt.fmt("UnhandledException", message=full_message))

            mes = core.MESException(
                message="Error in {}: {}".format(func_name, ex),
                user_message="An unexpected error occurred. Please contact support.",
                code="UNHANDLED",
                data={"inner": str(ex)}
            )
            return mes.user_message
    return wrapper