# -*- coding: utf-8 -*-
"""Domain events for the Line context."""
from __future__ import absolute_import

DEFAULT_METADATA = {}


class LineCreatedEvent(object):
    """Event emitted when a Line aggregate is created."""

    def __init__(self, identity, metadata=None):
        if identity is None:
            raise ValueError("Identity is required for events.")
        self._identity = identity
        self._metadata = metadata or dict(DEFAULT_METADATA)

    @property
    def identity(self):
        return self._identity

    @property
    def metadata(self):
        return self._metadata

    def to_dict(self):
        return {
            "identity": self._identity,
            "metadata": self._metadata,
        }
