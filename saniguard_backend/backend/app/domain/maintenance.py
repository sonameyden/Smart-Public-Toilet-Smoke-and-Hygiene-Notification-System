from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class MaintenanceType(str, Enum):
    PREVENTIVE = "preventive"
    CORRECTIVE = "corrective"


class MaintenanceStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class MaintenanceTicket:
    id: str
    type: MaintenanceType
    title: str
    description: str
    status: MaintenanceStatus
    assigned_to: Optional[str]
    notes: Optional[str]
    alert_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    def is_pending(self) -> bool:
        return self.status == MaintenanceStatus.PENDING

    def mark_complete(self) -> None:
        """Pure domain logic — no I/O."""
        self.status = MaintenanceStatus.COMPLETED
        self.updated_at = datetime.utcnow()
