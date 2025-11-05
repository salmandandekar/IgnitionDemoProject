# -*- coding: utf-8 -*-
"""Perspective message handler placeholder for Area context."""
from __future__ import absolute_import

import system.util

LOGGER = system.util.getLogger("core.area.ui.message_handlers.area_sync_handler")


def handle(session, payload):
    """Handle Perspective message for Area context."""
    LOGGER.warn("Placeholder handler invoked for Area context.")
    normalized = payload or {}
    return {
        "status": "NOT_IMPLEMENTED",
        "payload": normalized,
    }
