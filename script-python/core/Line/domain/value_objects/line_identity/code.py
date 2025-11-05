# -*- coding: utf-8 -*-
"""Value objects for the Line context."""
from __future__ import absolute_import

try:
    text_type = unicode
except NameError:  # pragma: no cover
    text_type = str


class LineIdentity(object):
    """Identity value object for the Line context."""

    def __init__(self, value):
        if value is None:
            raise ValueError("Identity value is required.")
        candidate = text_type(value).strip()
        if not candidate:
            raise ValueError("Identity value cannot be blank.")
        self._value = candidate

    @property
    def value(self):
        """Return the underlying identity value."""
        return self._value

    def __eq__(self, other):
        return bool(isinstance(other, LineIdentity) and self._value == other._value)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self._value)

    def __repr__(self):
        return "<LineIdentity value='{0}'>".format(self._value)
