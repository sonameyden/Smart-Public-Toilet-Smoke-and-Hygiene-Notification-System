from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class AlertType(str, Enum):
    SMOKE = "smoke"
    HYGIENE = "hygiene"
    MAINTENANCE = "maintenance"
    SYSTEM = "system"


class AlertSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AlertStatus(str, Enum):
    ACTIVE = "active"
    RESOLVED = "resolved"


@dataclass
class Alert:
    id: str
    type: AlertType
    severity: AlertSeverity
    status: AlertStatus
    title: str
    description: str
    location: str
    created_at: datetime
    resolved_by: Optional[str] = None
    resolved_at: Optional[datetime] = None

    def is_active(self) -> bool:
        return self.status == AlertStatus.ACTIVE

    def resolve(self, user_id: str) -> None:
        """Pure domain logic — does not touch the DB."""
        self.status = AlertStatus.RESOLVED
        self.resolved_by = user_id
        self.resolved_at = datetime.utcnow()
