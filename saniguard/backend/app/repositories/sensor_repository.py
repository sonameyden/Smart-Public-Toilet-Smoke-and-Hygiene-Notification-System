from typing import Optional
from datetime import datetime, timezone
from app.core.database import get_db
from app.repositories.base import BaseRepository


class SensorRepository(BaseRepository):

    @property
    def table(self) -> str:
        return "sensor_data"

    def insert(self, payload: dict) -> dict:
        payload["recorded_at"] = datetime.now(timezone.utc).isoformat()
        result = get_db().table(self.table).insert(payload).execute()
        return result.data[0]

    def get_latest(self) -> Optional[dict]:
        result = (
            get_db()
            .table(self.table)
            .select("*")
            .order("recorded_at", desc=True)
            .limit(1)
            .execute()
        )
        return result.data[0] if result.data else None

    def get_history(
        self,
        from_dt: Optional[datetime] = None,
        to_dt: Optional[datetime] = None,
        limit: int = 100,
    ) -> list[dict]:
        query = get_db().table(self.table).select("*").order("recorded_at", desc=True)
        if from_dt:
            query = query.gte("recorded_at", from_dt.isoformat())
        if to_dt:
            query = query.lte("recorded_at", to_dt.isoformat())
        result = query.limit(limit).execute()
        return result.data or []

    def get_air_quality_trend(self, days: int = 7) -> list[dict]:
        """Return average air_quality per day for the last N days."""
        from datetime import timedelta
        since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        result = (
            get_db()
            .table(self.table)
            .select("recorded_at, air_quality")
            .gte("recorded_at", since)
            .order("recorded_at")
            .execute()
        )
        return result.data or []


sensor_repository = SensorRepository()
