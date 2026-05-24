from fastapi import APIRouter, Depends
from app.schemas.settings import SystemSettingsOut, UpdateSettingsRequest
from app.services import settings_service
from app.services.auth_service import require_role
from app.domain.user import Role

router = APIRouter(prefix="/settings", tags=["settings"])

_admin_only = Depends(require_role(Role.ADMIN))


@router.get("", response_model=SystemSettingsOut, dependencies=[_admin_only])
def get_settings():
    return settings_service.get_settings()


@router.patch("", response_model=SystemSettingsOut, dependencies=[_admin_only])
def update_settings(req: UpdateSettingsRequest):
    return settings_service.update_settings(req)
