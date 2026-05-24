from typing import Optional
from app.cache.ttl_store import TTLStore
from app.cache.keys import SETTINGS

# Thresholds change rarely but must apply immediately when the admin updates them.
# TTL 60s covers normal polling; explicit invalidation handles the update case.
_TTL = 60.0

_store = TTLStore()


def get_settings() -> Optional[dict]:
    return _store.get(SETTINGS)


def set_settings(settings_dict: dict) -> None:
    _store.set(SETTINGS, settings_dict, _TTL)


def invalidate() -> None:
    """Call this immediately after a settings PATCH so new thresholds take effect."""
    _store.invalidate(SETTINGS)
