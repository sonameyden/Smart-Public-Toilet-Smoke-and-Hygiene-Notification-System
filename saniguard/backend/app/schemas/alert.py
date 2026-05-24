from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.domain.alert import AlertType, AlertSeverity, AlertStatus


class AlertOut(BaseModel):
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


class AlertResolveRequest(BaseModel):
    pass  # resolved_by is taken from the JWT token
