from typing import Optional
from fastapi import APIRouter, Depends, Query
from app.schemas.activity_log import ActivityLogOut
from app.services import activity_log_service
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/activity-logs", tags=["activity-logs"])


@router.get("", response_model=list[ActivityLogOut])
def get_activity_logs(
    limit: Optional[int] = Query(10, ge=1, le=100),
    _user=Depends(get_current_user),
):
    return activity_log_service.get_recent_activity(limit=limit)
