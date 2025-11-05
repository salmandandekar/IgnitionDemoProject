# -*- coding: utf-8 -*-
"""Query handler responsible for retrieving Site read models."""
from __future__ import absolute_import

from common.decorators.exception_logger import exception_logger
from common.decorators.tracing_decorator import tracing_decorator

LOGGER_NAME = "core.site.application.queries.get_site_query"


@exception_logger(LOGGER_NAME)
@tracing_decorator(LOGGER_NAME)
def execute(payload):
    """Return a placeholder response for a Site lookup."""
    normalized_payload = payload or {}
    response = {
        "siteCode": normalized_payload.get("siteCode"),
        "result": "NOT_IMPLEMENTED",
    }
    return response
