# -*- coding: utf-8 -*-
"""Perspective message handler placeholder for Workstation context."""
from __future__ import absolute_import

import system.util

LOGGER = system.util.getLogger("core.workstation.ui.message_handlers.workstation_sync_handler")


def handle(session, payload):
    """Handle Perspective message for Workstation context."""
    LOGGER.warn("Placeholder handler invoked for Workstation context.")
    normalized = payload or {}
    return {
        "status": "NOT_IMPLEMENTED",
        "payload": normalized,
    }
