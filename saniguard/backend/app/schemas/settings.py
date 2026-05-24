from typing import Optional
from pydantic import BaseModel


class SystemSettingsOut(BaseModel):
    smoke_threshold: float
    gas_threshold: float
    air_quality_threshold: float
    alert_notifications: bool
    auto_resolve_hours: int


class UpdateSettingsRequest(BaseModel):
    smoke_threshold: Optional[float] = None
    gas_threshold: Optional[float] = None
    air_quality_threshold: Optional[float] = None
    alert_notifications: Optional[bool] = None
    auto_resolve_hours: Optional[int] = None
