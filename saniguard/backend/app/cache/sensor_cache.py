from typing import Optional
from app.cache.ttl_store import TTLStore
from app.cache.keys import SENSOR_LATEST

# High-frequency MQTT writes mean the dashboard polls this constantly.
# 5-second TTL prevents hammering Supabase on every WebSocket refresh.
_TTL = 5.0

_store = TTLStore()


def get_latest() -> Optional[dict]:
    return _store.get(SENSOR_LATEST)


def set_latest(reading: dict) -> None:
    _store.set(SENSOR_LATEST, reading, _TTL)


def invalidate() -> None:
    _store.invalidate(SENSOR_LATEST)
