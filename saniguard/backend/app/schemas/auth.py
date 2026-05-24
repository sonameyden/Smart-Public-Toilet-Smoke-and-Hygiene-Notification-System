from pydantic import BaseModel, EmailStr
from app.domain.user import Role


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class DemoLoginRequest(BaseModel):
    role: Role


class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: Role = Role.VIEWER


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: Role
    user_id: str
    full_name: str
