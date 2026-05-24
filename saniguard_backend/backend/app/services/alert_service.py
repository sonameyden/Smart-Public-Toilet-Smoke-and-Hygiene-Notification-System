import asyncio
from app.repositories.alert_repository import alert_repository
from app.cache import alert_cache, analytics_cache
from app.core.websocket_manager import ws_manager
from app.domain.alert import AlertType, AlertSeverity, AlertStatus
from app.core.exceptions import NotFoundError, ForbiddenError
from app.schemas.alert import AlertOut


def _row_to_schema(row: dict) -> AlertOut:
    return AlertOut(**row)


def get_alerts(
    status: str | None = None,
    alert_type: str | None = None,
    severity: str | None = None,
) -> list[AlertOut]:
    rows = alert_repository.get_all(status=status, alert_type=alert_type, severity=severity)
    return [_row_to_schema(r) for r in rows]


def create_alert(
    alert_type: AlertType,
    severity: AlertSeverity,
    title: str,
    description: str,
    location: str = "IT Building Ground Floor",
) -> AlertOut | None:
    existing_active = alert_repository.get_all(
        alert_type=alert_type.value, status=AlertStatus.ACTIVE.value
    )
    if existing_active:
        return None

    row = alert_repository.create({
        "type": alert_type.value,
        "severity": severity.value,
        "status": AlertStatus.ACTIVE.value,
        "title": title,
        "description": description,
        "location": location,
    })
    alert_cache.invalidate()
    analytics_cache.invalidate_all()

    alert_out = _row_to_schema(row)
    asyncio.create_task(ws_manager.broadcast("new_alert", alert_out.model_dump(mode="json")))
    return alert_out


def resolve_alert(alert_id: str, resolved_by: str, user_role: str) -> AlertOut:
    existing = alert_repository.get_by_id(alert_id)
    if not existing:
        raise NotFoundError("Alert not found")
    if existing["status"] == AlertStatus.RESOLVED.value:
        raise ForbiddenError("Alert is already resolved")

    row = alert_repository.resolve(alert_id, resolved_by)
    if not row:
        raise NotFoundError("Alert could not be resolved")

    alert_cache.invalidate()
    analytics_cache.invalidate_all()

    alert_out = _row_to_schema(row)
    asyncio.create_task(ws_manager.broadcast("alert_resolved", alert_out.model_dump(mode="json")))
    return alert_out


def get_active_count() -> int:
    cached = alert_cache.get_active_count()
    if cached is not None:
        return cached
    count = alert_repository.count_active()
    alert_cache.set_active_count(count)
    return count