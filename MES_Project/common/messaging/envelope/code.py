
"""Utilities for constructing canonical messaging envelopes."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, MutableMapping, Optional

from ..utils import ids
from ..utils.timeutil import utc_now_iso


@dataclass(frozen=True)
class MessageEnvelope:
    """Immutable representation of a transport-agnostic message envelope."""

    verb: str
    noun: str
    data: Any
    correlation_id: str = field(default_factory=lambda: ids.new_id("corr"))
    timestamp: str = field(default_factory=utc_now_iso)
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "correlationId": self.correlation_id,
            "timestamp": self.timestamp,
            "verb": self.verb,
            "noun": self.noun,
            "data": self.data,
            "attributes": dict(self.attributes),
        }


def make(
    verb: str,
    noun: str,
    data: Any,
    correlation_id: Optional[str] = None,
    attributes: Optional[MutableMapping[str, Any]] = None,
) -> Dict[str, Any]:
    """Factory method preserved for backwards compatibility."""

    envelope = MessageEnvelope(
        verb=verb,
        noun=noun,
        data=data,
        correlation_id=correlation_id or ids.new_id("corr"),
        attributes=attributes or {},
    )
    return envelope.to_dict()
