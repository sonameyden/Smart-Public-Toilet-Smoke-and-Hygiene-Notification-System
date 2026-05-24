from typing import Optional
from datetime import datetime, timezone
from app.core.database import get_db
from app.repositories.base import BaseRepository


class ActivityLogRepository(BaseRepository):

    @property
    def table(self) -> str:
        return "activity_logs"

    def get_recent(self, limit: int = 10) -> list[dict]:
        result = (
            get_db()
            .table(self.table)
            .select("*")
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return result.data or []

    def create(self, payload: dict) -> dict:
        payload["created_at"] = datetime.now(timezone.utc).isoformat()
        result = get_db().table(self.table).insert(payload).execute()
        return result.data[0]


activity_log_repository = ActivityLogRepository()
