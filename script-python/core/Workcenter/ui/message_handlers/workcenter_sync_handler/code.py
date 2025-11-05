# -*- coding: utf-8 -*-
"""Perspective message handler placeholder for Workcenter context."""
from __future__ import absolute_import

import system.util

LOGGER = system.util.getLogger("core.workcenter.ui.message_handlers.workcenter_sync_handler")


def handle(session, payload):
    """Handle Perspective message for Workcenter context."""
    LOGGER.warn("Placeholder handler invoked for Workcenter context.")
    normalized = payload or {}
    return {
        "status": "NOT_IMPLEMENTED",
        "payload": normalized,
    }
