from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.domain.maintenance import MaintenanceType, MaintenanceStatus


class MaintenanceLogOut(BaseModel):
    id: str
    type: MaintenanceType
    title: str
    description: str
    status: MaintenanceStatus
    assigned_to: Optional[str] = None
    notes: Optional[str] = None
    alert_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class CreateMaintenanceLog(BaseModel):
    type: MaintenanceType
    title: str
    description: str
    assigned_to: Optional[str] = None
    alert_id: Optional[str] = None


class UpdateMaintenanceLog(BaseModel):
    status: Optional[MaintenanceStatus] = None
    notes: Optional[str] = None
    assigned_to: Optional[str] = None
