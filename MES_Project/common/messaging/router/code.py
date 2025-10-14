
"""Messaging router that orchestrates adapter selection.

Historically this module relied on module-level dictionaries and offered no
input validation, which meant that a typo in an adapter name or a misbehaving
handler could fail silently. This refactor brings the implementation closer to
the strategy pattern that is widely recommended for pluggable transports.

Key improvements:

* :class:`MessageAdapter` is now an abstract base class which ensures new
  adapters follow the publish/subscribe contract.
* :class:`InternalBus` guards its subscriber registry with a re-entrant lock,
  which prevents race conditions when multiple threads subscribe or publish.
* :class:`MessageRouter` encapsulates adapter registration, selection and
  logging while providing helpful error messages.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections import defaultdict
from threading import RLock
from typing import Callable, Dict, Iterable, List, MutableMapping, Optional

from ..logging.mes_logger import get_logger

log = get_logger("Router")

MessageHandler = Callable[[object], None]


class MessageAdapter(ABC):
    """Adapter contract for pluggable messaging implementations."""

    @abstractmethod
    def publish(self, topic: str, message: object) -> None:
        """Publish ``message`` to ``topic``."""

    @abstractmethod
    def subscribe(self, topic: str, handler: MessageHandler) -> None:
        """Register ``handler`` to consume messages from ``topic``."""


class InternalBus(MessageAdapter):
    """In-process pub/sub bus used for local development and tests."""

    def __init__(self) -> None:
        self._subscriptions: MutableMapping[str, List[MessageHandler]] = defaultdict(list)
        self._lock = RLock()

    def publish(self, topic: str, message: object) -> None:
        with self._lock:
            handlers: Iterable[MessageHandler] = tuple(self._subscriptions.get(topic, ()))
        handler_count = len(handlers)
        if handler_count == 0:
            log.debug("pub", extra={"topic": topic, "handlers": 0})
            return
        for handler in handlers:
            try:
                handler(message)
            except Exception:
                log.exception("handler-error", extra={"topic": topic, "handler": getattr(handler, "__name__", str(handler))})
        log.debug("pub", extra={"topic": topic, "handlers": handler_count})

    def subscribe(self, topic: str, handler: MessageHandler) -> None:
        if not callable(handler):
            raise TypeError("handler must be callable")
        with self._lock:
            subscribers = self._subscriptions[topic]
            subscribers.append(handler)
            count = len(subscribers)
        log.info("sub", extra={"topic": topic, "handlers": count})


class MessageRouter:
    """Thread-safe registry that manages the active adapter."""

    def __init__(self) -> None:
        self._adapters: Dict[str, MessageAdapter] = {}
        self._active: Optional[str] = None
        self._lock = RLock()
        # Always register the internal bus by default.
        self.register_adapter("internal", InternalBus(), activate=True)

    def register_adapter(self, name: str, adapter: MessageAdapter, activate: bool = False) -> None:
        if not name:
            raise ValueError("adapter name must be provided")
        if not isinstance(adapter, MessageAdapter):
            raise TypeError("adapter must implement MessageAdapter")
        with self._lock:
            self._adapters[name] = adapter
            if activate or self._active is None:
                self._active = name
        log.info("adapter-registered", extra={"adapter": name, "activate": activate})

    def use_adapter(self, name: str) -> None:
        with self._lock:
            if name not in self._adapters:
                raise ValueError(f"unknown adapter '{name}'")
            self._active = name
            adapter = self._adapters[name]
        log.info("using", extra={"adapter": name, "implementation": adapter.__class__.__name__})

    def _get_active(self) -> MessageAdapter:
        with self._lock:
            if self._active is None:
                raise RuntimeError("no message adapter has been activated")
            return self._adapters[self._active]

    def publish(self, topic: str, message: object) -> None:
        self._get_active().publish(topic, message)

    def subscribe(self, topic: str, handler: MessageHandler) -> None:
        self._get_active().subscribe(topic, handler)


_router = MessageRouter()


def register_adapter(name: str, adapter: MessageAdapter, activate: bool = False) -> None:
    """Expose :meth:`MessageRouter.register_adapter` at the module level."""

    _router.register_adapter(name, adapter, activate=activate)


def use_adapter(name: str) -> None:
    """Select the active messaging adapter."""

    _router.use_adapter(name)


def publish(topic: str, message: object) -> None:
    """Publish ``message`` to ``topic`` via the active adapter."""

    _router.publish(topic, message)


def subscribe(topic: str, handler: MessageHandler) -> None:
    """Subscribe ``handler`` to ``topic`` on the active adapter."""

    _router.subscribe(topic, handler)
