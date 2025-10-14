
"""Structured logging formatter that emits JSON payloads."""

from __future__ import annotations

import json
import logging
import time
from typing import Any, Dict

from ..decorators.tracing import get_correlation_id

_KNOWN_KEYS = ("cid", "func", "ms", "tenant", "site", "user")


class JsonFormatter(logging.Formatter):
    """Render log records as JSON-encoded dictionaries."""

    def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
        payload: Dict[str, Any] = {
            "ts": int(time.time() * 1000),
            "lvl": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        for key in _KNOWN_KEYS:
            if hasattr(record, key):
                payload[key] = getattr(record, key)
        payload.setdefault("cid", get_correlation_id())
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload)
