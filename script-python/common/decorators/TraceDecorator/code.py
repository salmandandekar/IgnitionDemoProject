import time, json
from functools import wraps
from common.logging import LogFactory
from common.logging import LogFormatter as fmt
from common.context import SessionContext

def traced(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        log = LogFactory.get_logger("Trace")

        # Safe session lookup
        try:
            ctx = SessionContext.current() or {}
        except Exception:
            ctx = {}

        correlation_id = ctx.get("correlationId", "N/A")
        tenant = ctx.get("tenant", "N/A")
        user = ctx.get("user", "N/A")

        def safe_json(data):
            try:
                s = json.dumps(data, default=str)
                return s[:400] + "..." if len(s) > 400 else s
            except Exception:
                return str(data)

        # Record entry
        log.debug(fmt.fmt(
            "ENTER",
            function=func.__name__,
            correlationId=correlation_id,
            tenant=tenant,
            user=user,
            args=safe_json(kwargs)
        ))

        start = time.time()
        status = "OK"
        result = None

        try:
            result = func(*args, **kwargs)
            return result
        except Exception:
            status = "ERROR"
            raise
        finally:
            duration = round((time.time() - start) * 1000, 2)
            log.debug(fmt.fmt(
                "EXIT",
                function=func.__name__,
                correlationId=correlation_id,
                tenant=tenant,
                user=user,
                status=status,
                duration="{} ms".format(duration),
                returnValue=safe_json(result)
            ))
    return wrapper