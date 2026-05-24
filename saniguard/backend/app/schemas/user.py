from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.domain.user import Role


class UserOut(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    role: Role
    is_active: bool
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None


class CreateUserRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: Role = Role.VIEWER


class UpdateUserRequest(BaseModel):
    full_name: Optional[str] = None
    role: Optional[Role] = None
    is_active: Optional[bool] = None
