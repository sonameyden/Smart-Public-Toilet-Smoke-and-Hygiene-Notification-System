from typing import Optional
from app.core.database import get_db
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):

    @property
    def table(self) -> str:
        return "users"

    def get_by_id(self, user_id: str) -> Optional[dict]:
        result = get_db().table(self.table).select("*").eq("id", user_id).execute()
        return result.data[0] if result.data else None

    def get_by_email(self, email: str) -> Optional[dict]:
        result = get_db().table(self.table).select("*").eq("email", email).execute()
        return result.data[0] if result.data else None

    def get_all(self) -> list[dict]:
        result = get_db().table(self.table).select("*").order("created_at", desc=True).execute()
        return result.data or []

    def create(self, payload: dict) -> dict:
        result = get_db().table(self.table).insert(payload).execute()
        return result.data[0]

    def update(self, user_id: str, payload: dict) -> Optional[dict]:
        result = (
            get_db().table(self.table).update(payload).eq("id", user_id).execute()
        )
        return result.data[0] if result.data else None

    def delete(self, user_id: str) -> None:
        get_db().table(self.table).delete().eq("id", user_id).execute()

    def update_last_login(self, user_id: str) -> None:
        from datetime import datetime, timezone
        get_db().table(self.table).update(
            {"last_login": datetime.now(timezone.utc).isoformat()}
        ).eq("id", user_id).execute()


user_repository = UserRepository()
