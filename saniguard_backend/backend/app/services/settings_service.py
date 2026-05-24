from app.repositories.settings_repository import settings_repository
from app.cache import settings_cache
from app.schemas.settings import SystemSettingsOut, UpdateSettingsRequest


def get_settings() -> SystemSettingsOut:
    cached = settings_cache.get_settings()
    if cached:
        return SystemSettingsOut(**cached)
    row = settings_repository.get()
    if row:
        settings_cache.set_settings(row)
        return SystemSettingsOut(**row)
    # Fallback defaults if table is empty
    return SystemSettingsOut(
        smoke_threshold=350.0,
        gas_threshold=100.0,
        air_quality_threshold=70.0,
        alert_notifications=True,
        auto_resolve_hours=24,
    )


def update_settings(req: UpdateSettingsRequest) -> SystemSettingsOut:
    updates = req.model_dump(exclude_none=True)
    updated = settings_repository.update(updates)
    # Invalidate immediately so next sensor reading uses new thresholds
    settings_cache.invalidate()
    return SystemSettingsOut(**updated)
