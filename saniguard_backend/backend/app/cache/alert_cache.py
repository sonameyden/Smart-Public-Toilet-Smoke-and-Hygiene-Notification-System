from typing import Optional
from app.cache.ttl_store import TTLStore
from app.cache.keys import ALERT_ACTIVE_COUNT

# Alert count shown on the dashboard badge — stale by max 10s.
# Explicitly invalidated when an alert is resolved so the badge updates immediately.
_TTL = 10.0

_store = TTLStore()


def get_active_count() -> Optional[int]:
    return _store.get(ALERT_ACTIVE_COUNT)


def set_active_count(count: int) -> None:
    _store.set(ALERT_ACTIVE_COUNT, count, _TTL)


def invalidate() -> None:
    """Call this immediately after resolving an alert."""
    _store.invalidate(ALERT_ACTIVE_COUNT)
