from fastapi import APIRouter, Depends
from app.schemas.user import UserOut, CreateUserRequest, UpdateUserRequest
from app.services.auth_service import require_role, hash_password
from app.repositories.user_repository import user_repository
from app.core.exceptions import NotFoundError, ConflictError
from app.domain.user import Role

router = APIRouter(prefix="/users", tags=["users"])

_admin_only = Depends(require_role(Role.ADMIN))


@router.get("", response_model=list[UserOut], dependencies=[_admin_only])
def get_users():
    return [UserOut(**u) for u in user_repository.get_all()]


@router.post("", response_model=UserOut, status_code=201, dependencies=[_admin_only])
def create_user(req: CreateUserRequest):
    if user_repository.get_by_email(req.email):
        raise ConflictError("Email already in use")
    from app.core.security import hash_password as hp
    row = user_repository.create({
        "full_name": req.full_name,
        "email": req.email,
        "password_hash": hp(req.password),
        "role": req.role.value,
        "is_active": True,
    })
    return UserOut(**row)


@router.patch("/{user_id}", response_model=UserOut, dependencies=[_admin_only])
def update_user(user_id: str, req: UpdateUserRequest):
    if not user_repository.get_by_id(user_id):
        raise NotFoundError("User not found")
    updates = req.model_dump(exclude_none=True)
    row = user_repository.update(user_id, updates)
    return UserOut(**row)


@router.delete("/{user_id}", status_code=204, dependencies=[_admin_only])
def delete_user(user_id: str):
    if not user_repository.get_by_id(user_id):
        raise NotFoundError("User not found")
    user_repository.delete(user_id)
