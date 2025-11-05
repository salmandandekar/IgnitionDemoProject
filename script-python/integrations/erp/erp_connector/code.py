# -*- coding: utf-8 -*-
"""ERP integration connector placeholder."""
from __future__ import absolute_import


class ErpConnector(object):
    """Translates data between Ignition and ERP systems."""

    def translate_outbound(self, payload):  # pragma: no cover - placeholder
        _ = payload or {}
        raise NotImplementedError

    def translate_inbound(self, payload):  # pragma: no cover - placeholder
        _ = payload or {}
        raise NotImplementedError
