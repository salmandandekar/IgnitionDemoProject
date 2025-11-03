"""QuestDB error logging utilities."""
import json
from datetime import datetime
from typing import Any, Dict, Optional

_INSERT_STATEMENT = (
    "INSERT INTO mes_error_log (ts, function_name, error_type, error_code, message, "
    "user_name, correlation_id, stacktrace, metadata) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
)


def _now() -> str:
    try:
        return datetime.utcnow().isoformat() + "Z"
    except Exception:
        return ""


def _get_context() -> Dict[str, Any]:
    try:
        from common.context import SessionContext  # type: ignore

        ctx = SessionContext.current()
        if isinstance(ctx, dict):
            return ctx
    except Exception:
        pass
    return {}


def _get_user(context: Dict[str, Any]) -> str:
    if context.get("user"):
        return str(context["user"])
    try:
        from system.util import getUserName  # type: ignore

        name = getUserName()
        if name:
            return str(name)
    except Exception:
        pass
    return "system"


def _stringify_mapping(mapping: Dict[str, Any]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for key, value in mapping.items():
        try:
            json.dumps(value)
            result[key] = value
        except Exception:
            result[key] = repr(value)
    return result


def log_exception(
    *,
    func_name: str,
    error_type: str,
    message: str,
    code: Optional[str] = None,
    stacktrace: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> bool:
    """Persist an exception record into QuestDB.

    The operation is best-effort: failures are swallowed to avoid cascading errors.
    """

    context = _get_context()
    payload_meta: Dict[str, Any] = {}
    if metadata:
        payload_meta.update(_stringify_mapping(metadata))

    payload = [
        _now(),
        func_name or "unknown",
        error_type or "Exception",
        code or "",
        message,
        _get_user(context),
        str(context.get("correlationId") or ""),
        stacktrace or "",
        json.dumps(payload_meta),
    ]

    try:
        from system.db import runPrepUpdate  # type: ignore

        runPrepUpdate(_INSERT_STATEMENT, payload)
        return True
    except Exception:
        return False
