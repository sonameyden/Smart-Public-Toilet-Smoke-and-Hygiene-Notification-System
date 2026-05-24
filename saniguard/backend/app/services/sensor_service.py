import asyncio
import logging
from typing import Optional

from app.repositories.sensor_repository import sensor_repository
from app.cache import sensor_cache
from app.core.websocket_manager import ws_manager
from app.services.settings_service import get_settings
from app.services.alert_service import create_alert
from app.domain.alert import AlertType, AlertSeverity
from app.domain.sensor import SensorReading
from app.schemas.sensor import LatestSensorOut, SensorReadingOut

logger = logging.getLogger(__name__)


def _status_label(value: float, threshold: float, inverted: bool = False) -> str:
    if inverted:
        return "normal" if value >= threshold else ("warning" if value >= threshold * 0.8 else "alert")
    margin = threshold * 0.8
    return "normal" if value <= margin else ("warning" if value <= threshold else "alert")


def get_latest() -> Optional[LatestSensorOut]:
    cached = sensor_cache.get_latest()
    if cached:
        return LatestSensorOut(**cached)

    row = sensor_repository.get_latest()
    if not row:
        return None

    settings = get_settings()
    out = _enrich_row(row, settings)
    sensor_cache.set_latest(out.model_dump(mode="json"))
    return out


def get_history(from_dt=None, to_dt=None, limit: int = 100) -> list[SensorReadingOut]:
    rows = sensor_repository.get_history(from_dt=from_dt, to_dt=to_dt, limit=limit)
    return [SensorReadingOut(**r) for r in rows]


async def process_mqtt_reading(topic: str, payload: dict) -> None:
    """
    Flow:
      1. Merge incoming topic into in-memory cache  (no DB call — microseconds)
      2. Broadcast to WebSocket immediately          (dashboard updates <50 ms)
      3. Persist to Supabase in background           (analytics/history, non-blocking)

    No backend debounce — the 200 ms frontend debounce in useSensorData.js
    already batches the 4 per-cycle broadcasts into a single React render,
    so adding a delay here would only make the displayed value older.
    """
    from app.core.mqtt import TOPIC_SMOKE, TOPIC_GAS, TOPIC_AIR_QUALITY, TOPIC_ENV

    # ── 1. Merge into in-memory cache ────────────────────────────────────────
    cached = sensor_cache.get_latest() or {}

    merged = {
        "smoke_ppm":   cached.get("smoke_ppm",   0.0),
        "gas_ppm":     cached.get("gas_ppm",      0.0),
        "air_quality": cached.get("air_quality",  100.0),
        "temperature": cached.get("temperature",  25.0),
        "humidity":    cached.get("humidity",     50.0),
        "location":    "IT Building Ground Floor",
    }

    if topic == TOPIC_SMOKE:
        merged["smoke_ppm"]   = payload.get("ppm",      merged["smoke_ppm"])
    elif topic == TOPIC_GAS:
        merged["gas_ppm"]     = payload.get("ppm",      merged["gas_ppm"])
    elif topic == TOPIC_AIR_QUALITY:
        merged["air_quality"] = payload.get("score",    merged["air_quality"])
    elif topic == TOPIC_ENV:
        merged["temperature"] = payload.get("temp",     merged["temperature"])
        merged["humidity"]    = payload.get("humidity", merged["humidity"])

    settings = get_settings()
    enriched = _enrich_row(merged, settings)
    sensor_cache.set_latest(enriched.model_dump(mode="json"))

    # ── 2. Broadcast immediately — no delay, no debounce ─────────────────────
    await ws_manager.broadcast("sensor_update", enriched.model_dump(mode="json"))

    # ── 3. Persist to Supabase in background ─────────────────────────────────
    asyncio.create_task(_persist_and_alert(merged, settings))


async def _persist_and_alert(merged: dict, settings) -> None:
    """Write to Supabase and check thresholds — runs after the UI has updated."""
    try:
        row = sensor_repository.insert(merged)
        logger.debug(f"Sensor reading persisted: id={row.get('id')}")
    except Exception as exc:
        logger.error(f"Failed to persist sensor reading: {exc}")
        return

    reading = SensorReading(**merged)
    if reading.is_smoke_alert(settings.smoke_threshold):
        create_alert(
            alert_type=AlertType.SMOKE,
            severity=AlertSeverity.HIGH,
            title="Smoke Level Elevated",
            description="Smoke sensor detected elevated levels in the toilet area",
        )
    elif reading.is_gas_alert(settings.gas_threshold):
        create_alert(
            alert_type=AlertType.HYGIENE,
            severity=AlertSeverity.MEDIUM,
            title="Gas Level Elevated",
            description="Gas sensor detected poor air quality in the toilet area",
        )
    elif reading.is_hygiene_warning(settings.air_quality_threshold):
        create_alert(
            alert_type=AlertType.HYGIENE,
            severity=AlertSeverity.MEDIUM,
            title="Cleaning Required",
            description="Toilet hygiene score dropped below threshold",
        )


def _enrich_row(row: dict, settings) -> LatestSensorOut:
    return LatestSensorOut(
        smoke_ppm=row["smoke_ppm"],
        gas_ppm=row["gas_ppm"],
        air_quality=row["air_quality"],
        temperature=row["temperature"],
        humidity=row["humidity"],
        location=row["location"],
        recorded_at=row.get("recorded_at"),
        smoke_status=_status_label(row["smoke_ppm"], settings.smoke_threshold),
        gas_status=_status_label(row["gas_ppm"], settings.gas_threshold),
        air_quality_status=_status_label(
            row["air_quality"], settings.air_quality_threshold, inverted=True
        ),
    )