# Centralized logger factory. No direct getLogger in business code.
def get_logger(name="MES"):
    try:
        from system.util import getLogger
        return getLogger(name)
    except Exception:
        # Minimal fallback logger with .info/.error methods
        class _L(object):
            def info(self, msg): pass
            def warn(self, msg): pass
            def error(self, msg): pass
            def debug(self, msg): pass
        return _L()
