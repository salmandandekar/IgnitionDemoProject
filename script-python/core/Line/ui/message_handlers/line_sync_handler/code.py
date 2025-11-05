# -*- coding: utf-8 -*-
"""Perspective message handler placeholder for Line context."""
from __future__ import absolute_import

import system.util

LOGGER = system.util.getLogger("core.line.ui.message_handlers.line_sync_handler")


def handle(session, payload):
    """Handle Perspective message for Line context."""
    LOGGER.warn("Placeholder handler invoked for Line context.")
    normalized = payload or {}
    return {
        "status": "NOT_IMPLEMENTED",
        "payload": normalized,
    }
