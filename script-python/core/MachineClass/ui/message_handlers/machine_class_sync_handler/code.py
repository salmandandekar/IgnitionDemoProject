# -*- coding: utf-8 -*-
"""Perspective message handler placeholder for MachineClass context."""
from __future__ import absolute_import

import system.util

LOGGER = system.util.getLogger("core.machine_class.ui.message_handlers.machine_class_sync_handler")


def handle(session, payload):
    """Handle Perspective message for MachineClass context."""
    LOGGER.warn("Placeholder handler invoked for MachineClass context.")
    normalized = payload or {}
    return {
        "status": "NOT_IMPLEMENTED",
        "payload": normalized,
    }
