from collections import defaultdict
from datetime import datetime, timezone

from app.repositories.alert_repository import alert_repository
from app.repositories.sensor_repository import sensor_repository
from app.cache import analytics_cache


def get_summary() -> dict:
    cached = analytics_cache.get_summary()
    if cached:
        return cached

    total = alert_repository.count_all()
    active = alert_repository.count_active()
    resolved = total - active

    # Count critical alerts
    critical_rows = alert_repository.get_all(severity="critical", status="active")
    critical = len(critical_rows)

    data = {
        "total_alerts": total,
        "active_alerts": active,
        "resolved_alerts": resolved,
        "critical_alerts": critical,
    }
    analytics_cache.set_summary(data)
    return data


def get_trends() -> list:
    cached = analytics_cache.get_trends()
    if cached:
        return cached

    raw = sensor_repository.get_air_quality_trend(days=7)

    # Group by date and average the air_quality score
    daily: dict[str, list[float]] = defaultdict(list)
    for row in raw:
        dt = row["recorded_at"]
        if isinstance(dt, str):
            dt = datetime.fromisoformat(dt.replace("Z", "+00:00"))
        day = dt.strftime("%a")  # Mon, Tue, ...
        daily[day].append(row["air_quality"])

    # Build ordered list for the chart
    day_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    data = [
        {
            "day": d,
            "avg_air_quality": round(sum(vals) / len(vals), 1) if vals else 0,
        }
        for d in day_order
        for vals in [daily.get(d, [])]
    ]
    analytics_cache.set_trends(data)
    return data


def get_hygiene_score() -> dict:
    cached = analytics_cache.get_hygiene_score()
    if cached:
        return cached

    raw = sensor_repository.get_air_quality_trend(days=7)
    if not raw:
        data = {"score": 0, "period": "weekly"}
    else:
        avg = sum(r["air_quality"] for r in raw) / len(raw)
        data = {"score": round(avg), "period": "weekly"}

    analytics_cache.set_hygiene_score(data)
    return data


def get_distribution() -> dict:
    cached = analytics_cache.get_distribution()
    if cached:
        return cached

    all_alerts = alert_repository.get_all()
    if not all_alerts:
        data = {"smoke": 0, "hygiene": 0, "maintenance": 0, "system": 0}
        analytics_cache.set_distribution(data)
        return data

    counts: dict[str, int] = defaultdict(int)
    for a in all_alerts:
        counts[a["type"]] += 1

    total = len(all_alerts)
    data = {
        "smoke":       round(counts.get("smoke", 0) / total * 100),
        "hygiene":     round(counts.get("hygiene", 0) / total * 100),
        "maintenance": round(counts.get("maintenance", 0) / total * 100),
        "system":      round(counts.get("system", 0) / total * 100),
    }
    analytics_cache.set_distribution(data)
    return data
