from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.role import Role
from app.schemas.role import RoleResponse
# from app.dependencies.auth import get_current_user
from app.middlewares.role_check import get_current_user
from app.db.deps import get_db
from app.exceptions.http_exceptions import AppException
from app.models.user import User

router = APIRouter()

@router.get("/roles", response_model=List[RoleResponse])
def get_all_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name.lower() != "superadmin":
        raise AppException(
            status_code=403,
            error_code="FORBIDDEN",
            error_message="You are not authorized to view roles"
        )

    roles = db.query(Role).all()
    return roles
