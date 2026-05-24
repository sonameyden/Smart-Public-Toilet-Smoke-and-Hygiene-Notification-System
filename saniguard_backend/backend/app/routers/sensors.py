from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Query
from app.schemas.sensor import LatestSensorOut, SensorReadingOut
from app.services import sensor_service
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/sensors", tags=["sensors"])


@router.get("/latest", response_model=Optional[LatestSensorOut])
def get_latest(_user=Depends(get_current_user)):
    return sensor_service.get_latest()


@router.get("/history", response_model=list[SensorReadingOut])
def get_history(
    from_dt: Optional[datetime] = Query(None),
    to_dt: Optional[datetime] = Query(None),
    limit: int = Query(100, le=500),
    _user=Depends(get_current_user),
):
    return sensor_service.get_history(from_dt=from_dt, to_dt=to_dt, limit=limit)
