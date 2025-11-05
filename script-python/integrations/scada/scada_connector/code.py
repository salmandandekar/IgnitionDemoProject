# -*- coding: utf-8 -*-
"""SCADA integration connector placeholder."""
from __future__ import absolute_import


class ScadaConnector(object):
    """Translates data between Ignition and SCADA systems."""

    def translate_outbound(self, payload):  # pragma: no cover - placeholder
        _ = payload or {}
        raise NotImplementedError

    def translate_inbound(self, payload):  # pragma: no cover - placeholder
        _ = payload or {}
        raise NotImplementedError
