# -*- coding: utf-8 -*-
"""Application command responsible for creating a Site aggregate."""
from __future__ import absolute_import

from common.decorators.exception_logger import exception_logger
from common.decorators.tracing_decorator import tracing_decorator

LOGGER_NAME = "core.site.application.commands.create_site_command"


@exception_logger(LOGGER_NAME)
@tracing_decorator(LOGGER_NAME)
def execute(payload):
    """Create a site using the provided payload."""
    normalized_payload = payload or {}
    response = {
        "status": "PENDING",
        "siteCode": normalized_payload.get("siteCode"),
        "siteName": normalized_payload.get("siteName"),
    }
    return response
