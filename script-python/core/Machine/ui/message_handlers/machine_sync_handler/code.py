# -*- coding: utf-8 -*-
"""Perspective message handler placeholder for Machine context."""
from __future__ import absolute_import

import system.util

LOGGER = system.util.getLogger("core.machine.ui.message_handlers.machine_sync_handler")


def handle(session, payload):
    """Handle Perspective message for Machine context."""
    LOGGER.warn("Placeholder handler invoked for Machine context.")
    normalized = payload or {}
    return {
        "status": "NOT_IMPLEMENTED",
        "payload": normalized,
    }
