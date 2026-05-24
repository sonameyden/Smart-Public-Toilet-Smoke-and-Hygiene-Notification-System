import time
from typing import Any, Optional


class TTLStore:
    """
    Lightweight in-memory key-value store with per-entry TTL.
    Uses time.monotonic() so it is not affected by system clock changes.

    Storage format:  { key: (value, expires_at_monotonic) }
    """

    def __init__(self):
        self._store: dict[str, tuple[Any, float]] = {}

    def get(self, key: str) -> Optional[Any]:
        """Return the cached value or None if missing / expired."""
        entry = self._store.get(key)
        if entry is None:
            return None
        value, expires_at = entry
        if time.monotonic() > expires_at:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: Any, ttl_seconds: float) -> None:
        """Store a value that expires after ttl_seconds."""
        self._store[key] = (value, time.monotonic() + ttl_seconds)

    def invalidate(self, key: str) -> None:
        """Delete a key immediately regardless of TTL (use after mutations)."""
        self._store.pop(key, None)

    def clear(self) -> None:
        self._store.clear()

    def __len__(self) -> int:
        return len(self._store)
