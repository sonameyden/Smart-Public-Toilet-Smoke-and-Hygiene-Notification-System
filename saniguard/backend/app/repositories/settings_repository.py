from typing import Optional
from app.core.database import get_db
from app.repositories.base import BaseRepository

_SETTINGS_ID = 1  # single-row config table


class SettingsRepository(BaseRepository):

    @property
    def table(self) -> str:
        return "system_settings"

    def get(self) -> Optional[dict]:
        result = (
            get_db().table(self.table).select("*").eq("id", _SETTINGS_ID).execute()
        )
        return result.data[0] if result.data else None

    def update(self, payload: dict) -> dict:
        from datetime import datetime, timezone
        payload["updated_at"] = datetime.now(timezone.utc).isoformat()
        result = (
            get_db()
            .table(self.table)
            .update(payload)
            .eq("id", _SETTINGS_ID)
            .execute()
        )
        return result.data[0]


settings_repository = SettingsRepository()
