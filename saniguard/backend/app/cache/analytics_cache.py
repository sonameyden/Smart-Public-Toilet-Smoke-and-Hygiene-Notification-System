from typing import Optional
from app.cache.ttl_store import TTLStore
from app.cache.keys import (
    ANALYTICS_SUMMARY,
    ANALYTICS_TRENDS,
    ANALYTICS_HYGIENE_SCORE,
    ANALYTICS_DISTRIBUTION,
)

# Analytics queries (GROUP BY, COUNT, AVG over sensor_data) are the most
# expensive DB operations. 5-minute TTL is acceptable since the analytics
# dashboard is not real-time — it shows trends, not live readings.
_TTL = 300.0

_store = TTLStore()


def get_summary() -> Optional[dict]:
    return _store.get(ANALYTICS_SUMMARY)


def set_summary(data: dict) -> None:
    _store.set(ANALYTICS_SUMMARY, data, _TTL)


def get_trends() -> Optional[list]:
    return _store.get(ANALYTICS_TRENDS)


def set_trends(data: list) -> None:
    _store.set(ANALYTICS_TRENDS, data, _TTL)


def get_hygiene_score() -> Optional[dict]:
    return _store.get(ANALYTICS_HYGIENE_SCORE)


def set_hygiene_score(data: dict) -> None:
    _store.set(ANALYTICS_HYGIENE_SCORE, data, _TTL)


def get_distribution() -> Optional[dict]:
    return _store.get(ANALYTICS_DISTRIBUTION)


def set_distribution(data: dict) -> None:
    _store.set(ANALYTICS_DISTRIBUTION, data, _TTL)


def invalidate_all() -> None:
    """Clear all analytics cache entries (e.g. after an alert is resolved)."""
    for key in (ANALYTICS_SUMMARY, ANALYTICS_TRENDS, ANALYTICS_HYGIENE_SCORE, ANALYTICS_DISTRIBUTION):
        _store.invalidate(key)
