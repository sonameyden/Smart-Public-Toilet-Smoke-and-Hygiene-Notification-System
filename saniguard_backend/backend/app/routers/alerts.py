from typing import Optional
from fastapi import APIRouter, Depends, Query
from app.schemas.alert import AlertOut
from app.services import alert_service
from app.services.auth_service import get_current_user, require_role
from app.domain.user import Role

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertOut])
def get_alerts(
    status: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    _user=Depends(get_current_user),
):
    return alert_service.get_alerts(status=status, alert_type=type, severity=severity)


@router.patch(
    "/{alert_id}/resolve",
    response_model=AlertOut,
    dependencies=[Depends(require_role(Role.ADMIN, Role.MAINTENANCE))],
)
async def resolve_alert(
    alert_id: str,
    current_user=Depends(get_current_user),
):
    return alert_service.resolve_alert(
        alert_id=alert_id,
        resolved_by=current_user["id"],
        user_role=current_user["role"],
    )
