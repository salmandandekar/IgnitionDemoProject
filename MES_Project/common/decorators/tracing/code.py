
"""Tracing helpers that enrich log events with correlation information."""

from __future__ import annotations

import functools
import threading
import time
import uuid
from typing import Any, Callable, Optional, TypeVar

from ..logging.mes_logger import get_logger

F = TypeVar("F", bound=Callable[..., Any])

_THREAD = threading.local()


def get_correlation_id() -> Optional[str]:
    """Return the correlation identifier associated with the current thread."""

    return getattr(_THREAD, "cid", None)


def with_correlation(correlation_id: Optional[str] = None) -> Callable[[F], F]:
    """Ensure the decorated function executes with a correlation identifier."""

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any):  # type: ignore[misc]
            previous = getattr(_THREAD, "cid", None)
            try:
                _THREAD.cid = correlation_id or previous or str(uuid.uuid4())
                return func(*args, **kwargs)
            finally:
                if previous is None:
                    _THREAD.__dict__.pop("cid", None)
                else:
                    _THREAD.cid = previous

        return wrapper  # type: ignore[return-value]

    return decorator


def traced(logger_name: Optional[str] = None) -> Callable[[F], F]:
    """Log execution boundaries and duration for the wrapped callable."""

    log = get_logger(logger_name or "trace")

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any):  # type: ignore[misc]
            correlation = get_correlation_id() or str(uuid.uuid4())
            start = time.time()
            log.debug("start", extra={"cid": correlation, "func": func.__name__})
            try:
                result = func(*args, **kwargs)
            except Exception:
                log.exception("fail", extra={"cid": correlation, "func": func.__name__})
                raise
            duration_ms = round((time.time() - start) * 1000, 2)
            log.info("ok", extra={"cid": correlation, "func": func.__name__, "ms": duration_ms})
            return result

        return wrapper  # type: ignore[return-value]

    return decorator
