from common.logging.LogFactory import code as LogFactory
from common.logging.LogFormatter import code as fmt
from common.context.SessionContext import code as Session

def traced(func):
    def wrapper(*args, **kwargs):
        log = LogFactory.get_logger("Trace")
        ctx = Session.current()
        log.debug(fmt.fmt("ENTER", function=func.__name__, correlationId=ctx.get("correlationId")))
        try:
            result = func(*args, **kwargs)
            log.debug(fmt.fmt("EXIT", function=func.__name__, correlationId=ctx.get("correlationId")))
            return result
        except Exception as ex:
            # do not print; let ExceptionHandlerDecorator handle error logging
            raise
    return wrapper
