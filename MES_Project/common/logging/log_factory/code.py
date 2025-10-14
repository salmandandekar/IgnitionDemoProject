
"""Centralised logging configuration for the MES project."""

from __future__ import annotations

import logging
import sys
from threading import RLock
from typing import Optional

from .log_formatter import JsonFormatter

_configured = False
_lock = RLock()


def configure_root(level: Optional[int] = None) -> None:
    """Initialise the root logger with a JSON formatter.

    The function is idempotent and safe to call from multiple threads.
    """

    global _configured
    with _lock:
        if _configured:
            return
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        root_logger = logging.getLogger()
        root_logger.setLevel(level or logging.INFO)
        root_logger.addHandler(handler)
        _configured = True
