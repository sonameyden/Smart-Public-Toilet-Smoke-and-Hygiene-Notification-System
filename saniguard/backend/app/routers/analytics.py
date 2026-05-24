from fastapi import APIRouter, Depends
from app.services import analytics_service
from app.services.auth_service import require_role
from app.domain.user import Role

router = APIRouter(prefix="/analytics", tags=["analytics"])

_admin_only = Depends(require_role(Role.ADMIN))


@router.get("/summary", dependencies=[_admin_only])
def get_summary():
    return analytics_service.get_summary()


@router.get("/trends", dependencies=[_admin_only])
def get_trends():
    return analytics_service.get_trends()


@router.get("/hygiene-score", dependencies=[_admin_only])
def get_hygiene_score():
    return analytics_service.get_hygiene_score()


@router.get("/distribution", dependencies=[_admin_only])
def get_distribution():
    return analytics_service.get_distribution()
