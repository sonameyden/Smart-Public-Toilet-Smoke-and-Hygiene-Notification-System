from fastapi import APIRouter, Depends
from app.schemas.maintenance import MaintenanceLogOut, CreateMaintenanceLog, UpdateMaintenanceLog
from app.services import maintenance_service
from app.services.auth_service import get_current_user, require_role
from app.domain.user import Role

router = APIRouter(prefix="/maintenance", tags=["maintenance"])


@router.get(
    "/logs",
    response_model=list[MaintenanceLogOut],
    dependencies=[Depends(require_role(Role.ADMIN, Role.MAINTENANCE))],
)
def get_logs(current_user=Depends(get_current_user)):
    return maintenance_service.get_logs(
        user_id=current_user["id"], role=current_user["role"]
    )


@router.post(
    "/logs",
    response_model=MaintenanceLogOut,
    status_code=201,
    dependencies=[Depends(require_role(Role.ADMIN))],
)
def create_log(req: CreateMaintenanceLog):
    return maintenance_service.create_log(req)


@router.patch(
    "/logs/{log_id}",
    response_model=MaintenanceLogOut,
    dependencies=[Depends(require_role(Role.ADMIN, Role.MAINTENANCE))],
)
def update_log(
    log_id: str,
    req: UpdateMaintenanceLog,
    current_user=Depends(get_current_user),
):
    return maintenance_service.update_log(
        log_id=log_id,
        req=req,
        user_id=current_user["id"],
        role=current_user["role"],
    )
