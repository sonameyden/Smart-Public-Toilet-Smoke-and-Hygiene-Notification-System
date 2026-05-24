from fastapi import APIRouter
from app.schemas.auth import LoginRequest, RegisterRequest, DemoLoginRequest, TokenResponse
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest):
    return auth_service.login(req.email, req.password)


@router.post("/demo-login", response_model=TokenResponse)
def demo_login(req: DemoLoginRequest):
    return auth_service.demo_login(req.role)


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(req: RegisterRequest):
    return auth_service.register(req.full_name, req.email, req.password, req.role)
