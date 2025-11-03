import traceback
from common.logging import LogFactory
from common.logging import LogFormatter as fmt
from common.exceptions import MESException as core


def _safe_metadata(args, kwargs, extra=None):
    metadata = {
        "args": [repr(arg) for arg in args],
        "kwargs": {key: repr(value) for key, value in kwargs.items()},
    }
    if extra:
        metadata.update(extra)
    return metadata


def _log_to_questdb(**payload):
    try:
        from common.logging.QuestDbLogger import code as quest_logger
    except Exception:
        return False

    try:
        return quest_logger.log_exception(**payload)
    except Exception:
        return False

def guarded(func):
    def wrapper(*args, **kwargs):
        log = LogFactory.get_logger("Errors")
        func_name = getattr(func, "__name__", "unknown")
        try:
            return func(*args, **kwargs)

        except core.MESException as ex:
            message = "{}: {}".format(func_name, ex)
            log.error(fmt.fmt(
                "MESException",
                code=ex.code,
                message=message
            ))
            _log_to_questdb(
                func_name=func_name,
                error_type="MESException",
                code=ex.code,
                message=message,
                metadata=_safe_metadata(args, kwargs, {"data": ex.data})
            )
            return ex.user_message

        except Exception as ex:
            # Combine summary + traceback into one single message
            tb_str = traceback.format_exc()
            full_message = "{} failed: {}\n{}".format(func_name, ex, tb_str)
            log.error(fmt.fmt("UnhandledException", message=full_message))

            _log_to_questdb(
                func_name=func_name,
                error_type=ex.__class__.__name__,
                code="UNHANDLED",
                message=str(ex),
                stacktrace=tb_str,
                metadata=_safe_metadata(args, kwargs)
            )

            mes = core.MESException(
                message="Error in {}: {}".format(func_name, ex),
                user_message="An unexpected error occurred. Please contact support.",
                code="UNHANDLED",
                data={"inner": str(ex)}
            )
            return mes.user_message
    return wrapper