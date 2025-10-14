
"""Cache provider abstraction used by the MES demo project.

The previous iteration of this module exposed a couple of module-level helper
functions that proxied to a globally-instantiated ``InMemoryCache``. While that
approach worked, it made unit testing and provider swaps unnecessarily
error-prone: there was no guard rail ensuring that a custom provider actually
implemented the expected interface, and replacing the provider mid-flight was
not thread safe.

To bring the implementation closer to commonly accepted enterprise standards we
introduce three improvements:

* Use :class:`abc.ABC` to formalise the cache provider contract.
* Wrap the active provider in a lightweight registry object that synchronises
  updates with :class:`threading.RLock`.
* Honour the optional ``ttl`` argument by expiring cached items and cleaning up
  stale entries on reads.

This keeps the public ``get``/``set``/``use_provider`` functions intact for
callers inside the project while ensuring consistent behaviour across
providers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from threading import RLock
from time import monotonic
from typing import Any, Dict, Optional

from ..logging.mes_logger import get_logger

log = get_logger("Cache")


class CacheProvider(ABC):
    """Defines the contract every cache implementation must satisfy."""

    @abstractmethod
    def get(self, region: str, key: str) -> Any:
        """Return the cached value for ``key`` inside ``region`` if present."""

    @abstractmethod
    def set(self, region: str, key: str, value: Any, ttl: Optional[float] = None) -> bool:
        """Store ``value`` under ``key`` for ``region``.

        The ``ttl`` parameter is expressed in seconds. Providers that do not
        support expirations should simply ignore the parameter.
        """

    @abstractmethod
    def clear(self, region: Optional[str] = None, key: Optional[str] = None) -> None:
        """Evict entries from the cache."""


@dataclass
class _CacheEntry:
    value: Any
    expires_at: Optional[float]

    def is_expired(self) -> bool:
        return self.expires_at is not None and monotonic() >= self.expires_at


class InMemoryCache(CacheProvider):
    """Thread-safe cache backed by a nested dictionary.

    The implementation is intentionally simple yet robust enough for unit tests
    and offline development. Expiry timestamps leverage ``time.monotonic`` so
    they are not affected by system clock adjustments.
    """

    def __init__(self) -> None:
        self._regions: Dict[str, Dict[str, _CacheEntry]] = {}
        self._lock = RLock()

    def _cleanup_locked(self, region: str) -> None:
        bucket = self._regions.get(region)
        if not bucket:
            return
        expired_keys = [k for k, entry in bucket.items() if entry.is_expired()]
        for key in expired_keys:
            del bucket[key]
        if not bucket:
            self._regions.pop(region, None)

    def get(self, region: str, key: str) -> Any:
        with self._lock:
            self._cleanup_locked(region)
            entry = self._regions.get(region, {}).get(key)
            if entry and not entry.is_expired():
                return entry.value
            if entry and entry.is_expired():
                # Remove expired entry on access to avoid returning stale data.
                del self._regions[region][key]
            return None

    def set(self, region: str, key: str, value: Any, ttl: Optional[float] = None) -> bool:
        expires_at = monotonic() + ttl if ttl else None
        with self._lock:
            bucket = self._regions.setdefault(region, {})
            bucket[key] = _CacheEntry(value=value, expires_at=expires_at)
        return True

    def clear(self, region: Optional[str] = None, key: Optional[str] = None) -> None:
        with self._lock:
            if region is None:
                self._regions.clear()
                return
            if key is None:
                self._regions.pop(region, None)
                return
            bucket = self._regions.get(region)
            if bucket and key in bucket:
                del bucket[key]
                if not bucket:
                    self._regions.pop(region, None)


class _CacheRegistry:
    """Maintains the active cache provider for the current runtime."""

    def __init__(self) -> None:
        self._lock = RLock()
        self._provider: CacheProvider = InMemoryCache()

    def get_provider(self) -> CacheProvider:
        with self._lock:
            return self._provider

    def use_provider(self, provider: Optional[CacheProvider]) -> CacheProvider:
        if provider is not None and not isinstance(provider, CacheProvider):
            raise TypeError("provider must implement CacheProvider")
        with self._lock:
            if provider is None:
                # Reset to the default provider when ``None`` is supplied.
                self._provider = InMemoryCache()
            else:
                self._provider = provider
            active = self._provider
        log.info("provider-set", extra={"provider": active.__class__.__name__})
        return active


_registry = _CacheRegistry()


def use_provider(provider: Optional[CacheProvider]) -> CacheProvider:
    """Switch the active cache provider.

    Passing ``None`` reverts to the built-in :class:`InMemoryCache`.
    """

    return _registry.use_provider(provider)


def get(region: str, key: str) -> Any:
    """Retrieve a cached value via the active provider."""

    return _registry.get_provider().get(region, key)


def set(region: str, key: str, value: Any, ttl: Optional[float] = None) -> bool:
    """Persist a value in the active cache provider."""

    return _registry.get_provider().set(region, key, value, ttl)


def clear(region: Optional[str] = None, key: Optional[str] = None) -> None:
    """Expose the provider ``clear`` method for convenience."""

    _registry.get_provider().clear(region=region, key=key)
