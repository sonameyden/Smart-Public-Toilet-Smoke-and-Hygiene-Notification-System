from typing import Optional
from datetime import datetime, timezone
from app.core.database import get_db
from app.repositories.base import BaseRepository


class AlertRepository(BaseRepository):

    @property
    def table(self) -> str:
        return "alerts"

    def get_all(
        self,
        status: Optional[str] = None,
        alert_type: Optional[str] = None,
        severity: Optional[str] = None,
    ) -> list[dict]:
        query = get_db().table(self.table).select("*").order("created_at", desc=True)
        if status:
            query = query.eq("status", status)
        if alert_type:
            query = query.eq("type", alert_type)
        if severity:
            query = query.eq("severity", severity)
        return query.execute().data or []

    def get_by_id(self, alert_id: str) -> Optional[dict]:
        result = get_db().table(self.table).select("*").eq("id", alert_id).execute()
        return result.data[0] if result.data else None

    def create(self, payload: dict) -> dict:
        payload["created_at"] = datetime.now(timezone.utc).isoformat()
        result = get_db().table(self.table).insert(payload).execute()
        return result.data[0]

    def resolve(self, alert_id: str, resolved_by: str) -> Optional[dict]:
        payload = {
            "status": "resolved",
            "resolved_by": resolved_by,
            "resolved_at": datetime.now(timezone.utc).isoformat(),
        }
        result = (
            get_db().table(self.table).update(payload).eq("id", alert_id).execute()
        )
        return result.data[0] if result.data else None

    def count_active(self) -> int:
        result = (
            get_db()
            .table(self.table)
            .select("id", count="exact")
            .eq("status", "active")
            .execute()
        )
        return result.count or 0

    def count_all(self) -> int:
        result = (
            get_db().table(self.table).select("id", count="exact").execute()
        )
        return result.count or 0


alert_repository = AlertRepository()
