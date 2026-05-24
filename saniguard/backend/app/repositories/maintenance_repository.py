from typing import Optional
from datetime import datetime, timezone
from app.core.database import get_db
from app.repositories.base import BaseRepository


class MaintenanceRepository(BaseRepository):

    @property
    def table(self) -> str:
        return "maintenance_logs"

    def get_all(self, assigned_to: Optional[str] = None) -> list[dict]:
        query = get_db().table(self.table).select("*").order("created_at", desc=True)
        if assigned_to:
            query = query.eq("assigned_to", assigned_to)
        return query.execute().data or []

    def get_by_id(self, log_id: str) -> Optional[dict]:
        result = get_db().table(self.table).select("*").eq("id", log_id).execute()
        return result.data[0] if result.data else None

    def create(self, payload: dict) -> dict:
        now = datetime.now(timezone.utc).isoformat()
        payload["created_at"] = now
        payload["updated_at"] = now
        payload.setdefault("status", "pending")
        result = get_db().table(self.table).insert(payload).execute()
        return result.data[0]

    def update(self, log_id: str, payload: dict) -> Optional[dict]:
        payload["updated_at"] = datetime.now(timezone.utc).isoformat()
        result = (
            get_db().table(self.table).update(payload).eq("id", log_id).execute()
        )
        return result.data[0] if result.data else None

    def count_pending(self) -> int:
        result = (
            get_db()
            .table(self.table)
            .select("id", count="exact")
            .eq("status", "pending")
            .execute()
        )
        return result.count or 0


maintenance_repository = MaintenanceRepository()
