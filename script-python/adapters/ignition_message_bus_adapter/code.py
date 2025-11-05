# -*- coding: utf-8 -*-
"""message bus adapter placeholder."""
from __future__ import absolute_import

import system.util


class MessageBusAdapter(object):
    """Implements gateway-facing behavior using Ignition services."""

    def __init__(self):
        self._logger = system.util.getLogger("adapters.ignition_message_bus_adapter")

    def execute(self, payload):  # pragma: no cover - placeholder
        _ = payload or {}
        self._logger.warn("Adapter message bus not implemented.")
        raise NotImplementedError
