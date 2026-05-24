from app.repositories.maintenance_repository import maintenance_repository
from app.core.exceptions import NotFoundError, ForbiddenError
from app.domain.user import Role
from app.schemas.maintenance import (
    MaintenanceLogOut,
    CreateMaintenanceLog,
    UpdateMaintenanceLog,
)


def _row_to_schema(row: dict) -> MaintenanceLogOut:
    return MaintenanceLogOut(**row)


def get_logs(user_id: str, role: str) -> list[MaintenanceLogOut]:
    # Maintenance staff only sees logs assigned to them;
    # admins see everything.
    assigned_filter = user_id if role == Role.MAINTENANCE.value else None
    rows = maintenance_repository.get_all(assigned_to=assigned_filter)
    return [_row_to_schema(r) for r in rows]


def create_log(req: CreateMaintenanceLog) -> MaintenanceLogOut:
    row = maintenance_repository.create(req.model_dump(exclude_none=True))
    return _row_to_schema(row)


def update_log(
    log_id: str,
    req: UpdateMaintenanceLog,
    user_id: str,
    role: str,
) -> MaintenanceLogOut:
    existing = maintenance_repository.get_by_id(log_id)
    if not existing:
        raise NotFoundError("Maintenance log not found")

    # Maintenance staff can only update logs assigned to themselves
    if (
        role == Role.MAINTENANCE.value
        and existing.get("assigned_to") != user_id
    ):
        raise ForbiddenError("You can only update logs assigned to you")

    updates = req.model_dump(exclude_none=True)
    row = maintenance_repository.update(log_id, updates)
    return _row_to_schema(row)
