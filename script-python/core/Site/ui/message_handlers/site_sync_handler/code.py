# -*- coding: utf-8 -*-
"""Perspective message handler scaffold for Site synchronization."""
from __future__ import absolute_import

from common.decorators.exception_logger import exception_logger
from common.decorators.tracing_decorator import tracing_decorator

LOGGER_NAME = "core.site.ui.message_handlers.site_sync_handler"


@exception_logger(LOGGER_NAME)
@tracing_decorator(LOGGER_NAME)
def handle(session, payload):
    """Process inbound Site sync messages."""
    del session
    normalized_payload = payload or {}
    return {
        "status": "RECEIVED",
        "siteCode": normalized_payload.get("siteCode"),
    }
