from app.repositories.activity_log_repository import activity_log_repository
from app.schemas.activity_log import ActivityLogOut
from app.domain.activity_log import ActivityType


def _row_to_schema(row: dict) -> ActivityLogOut:
    return ActivityLogOut(**row)


def get_recent_activity(limit: int = 10) -> list[ActivityLogOut]:
    rows = activity_log_repository.get_recent(limit=limit)
    return [_row_to_schema(r) for r in rows]


def log_activity(
    action: str,
    username: str,
    role: str,
    activity_type: ActivityType,
) -> ActivityLogOut:
    row = activity_log_repository.create({
        "action": action,
        "username": username,
        "role": role,
        "type": activity_type.value,
    })
    return _row_to_schema(row)
