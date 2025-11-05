# -*- coding: utf-8 -*-
"""Perspective message handler placeholder for Enterprise context."""
from __future__ import absolute_import

import system.util

LOGGER = system.util.getLogger("core.enterprise.ui.message_handlers.enterprise_sync_handler")


def handle(session, payload):
    """Handle Perspective message for Enterprise context."""
    LOGGER.warn("Placeholder handler invoked for Enterprise context.")
    normalized = payload or {}
    return {
        "status": "NOT_IMPLEMENTED",
        "payload": normalized,
    }
