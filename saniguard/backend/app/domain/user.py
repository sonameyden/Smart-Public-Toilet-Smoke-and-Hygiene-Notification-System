from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import datetime


class Role(str, Enum):
    ADMIN = "admin"
    MAINTENANCE = "maintenance"
    VIEWER = "viewer"


@dataclass
class User:
    id: str
    full_name: str
    email: str
    role: Role
    is_active: bool = True
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None

    def can_resolve_alerts(self) -> bool:
        return self.role in (Role.ADMIN, Role.MAINTENANCE)

    def can_manage_users(self) -> bool:
        return self.role == Role.ADMIN

    def can_view_analytics(self) -> bool:
        return self.role == Role.ADMIN

    def can_change_settings(self) -> bool:
        return self.role == Role.ADMIN
