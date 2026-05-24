from typing import Optional
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.core.exceptions import UnauthorizedError, ConflictError, ForbiddenError
from app.repositories.user_repository import user_repository
from app.domain.user import Role
from app.schemas.auth import TokenResponse

_DEMO_CREDENTIALS = {
    Role.ADMIN: {"email": "admin@campus.edu", "password": "demo1234"},
    Role.MAINTENANCE: {"email": "maintenance@campus.edu", "password": "demo1234"},
    Role.VIEWER: {"email": "authority@campus.edu", "password": "demo1234"},
}

_bearer = HTTPBearer(auto_error=False)


def login(email: str, password: str) -> TokenResponse:
    user = user_repository.get_by_email(email)
    if not user or not verify_password(password, user["password_hash"]):
        raise UnauthorizedError("Invalid email or password")
    if not user["is_active"]:
        raise ForbiddenError("Account is deactivated")
    user_repository.update_last_login(user["id"])
    token = create_access_token({"sub": user["id"], "role": user["role"]})
    return TokenResponse(
        access_token=token,
        role=user["role"],
        user_id=user["id"],
        full_name=user["full_name"],
    )


def demo_login(role: Role) -> TokenResponse:
    creds = _DEMO_CREDENTIALS[role]

    # Ensure demo user exists in DB. If not, create it so demo-login works
    existing = user_repository.get_by_email(creds["email"])
    if not existing:
        # create a demo user with the provided role
        hashed = hash_password(creds["password"])
        demo_user = user_repository.create({
            "full_name": f"Demo {role.value.capitalize()}",
            "email": creds["email"],
            "password_hash": hashed,
            "role": role.value,
            "is_active": True,
        })
        # proceed to generate token for the created user
        token = create_access_token({"sub": demo_user["id"], "role": demo_user["role"]})
        return TokenResponse(
            access_token=token,
            role=demo_user["role"],
            user_id=demo_user["id"],
            full_name=demo_user["full_name"],
        )

    # fallback to standard login if user exists
    return login(creds["email"], creds["password"])


def register(full_name: str, email: str, password: str, role: Role) -> TokenResponse:
    if user_repository.get_by_email(email):
        raise ConflictError("An account with this email already exists")
    hashed = hash_password(password)
    new_user = user_repository.create({
        "full_name": full_name,
        "email": email,
        "password_hash": hashed,
        "role": role.value,
        "is_active": True,
    })
    token = create_access_token({"sub": new_user["id"], "role": new_user["role"]})
    return TokenResponse(
        access_token=token,
        role=new_user["role"],
        user_id=new_user["id"],
        full_name=new_user["full_name"],
    )


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer),
) -> dict:
    if not credentials:
        raise UnauthorizedError()
    payload = decode_access_token(credentials.credentials)
    if not payload:
        raise UnauthorizedError("Invalid or expired token")
    user = user_repository.get_by_id(payload["sub"])
    if not user or not user["is_active"]:
        raise UnauthorizedError()
    return user


def require_role(*roles: Role):
    """FastAPI dependency factory — enforces RBAC at the router level."""
    def _check(current_user: dict = Depends(get_current_user)) -> dict:
        if current_user["role"] not in [r.value for r in roles]:
            raise ForbiddenError()
        return current_user
    return _check
