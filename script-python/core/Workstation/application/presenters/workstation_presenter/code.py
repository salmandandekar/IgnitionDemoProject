# -*- coding: utf-8 -*-
"""Presenter helpers for the Workstation context."""
from __future__ import absolute_import


def workstation_present(response):
    """Project a response into a presenter-friendly structure."""
    normalized = response or {}
    return {
        "status": normalized.get("status", "UNKNOWN"),
        "payload": normalized.get("payload", {}),
    }
