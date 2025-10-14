
"""Utility for retrieving configured loggers within the MES project."""

from __future__ import annotations

import logging
from typing import Optional

from .log_factory import configure_root


def get_logger(name: Optional[str] = "MES") -> logging.Logger:
    """Return a logger initialised with the project's JSON formatter."""

    configure_root()
    return logging.getLogger(name)
