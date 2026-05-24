from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SensorReadingOut(BaseModel):
    id: int
    smoke_ppm: float
    gas_ppm: float
    air_quality: float
    temperature: float
    humidity: float
    location: str
    recorded_at: datetime


class LatestSensorOut(BaseModel):
    smoke_ppm: float
    gas_ppm: float
    air_quality: float
    temperature: float
    humidity: float
    location: str
    recorded_at: Optional[datetime]
    smoke_status: str   # "normal" | "warning" | "alert"
    gas_status: str
    air_quality_status: str
