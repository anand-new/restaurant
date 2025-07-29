from fastapi import Depends, HTTPException, status
from app.core.jwt import decode_token
from fastapi.security import OAuth2PasswordBearer
from app.db.deps import get_db
from app.exceptions.http_exceptions import AppException
from app.models.user import User
from app.services.user_service import get_user_by_id
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = decode_token(token)
    if not payload:
        raise AppException(
            status_code=401,
            error_code="INVALID_TOKEN",
            error_message="Invalid token"
        )

    user = db.query(User).filter(User.id == payload.get("user_id")).first()
    if not user:
        raise AppException(
            status_code=404,
            error_code="USER_NOT_FOUND",
            error_message="User not found"
        )

    # Optional: assert tenant_id from token matches user.tenant_id
    token_tenant_id = payload.get("tenant_id")
    if token_tenant_id and str(user.tenant_id) != str(token_tenant_id):
        raise AppException(
            status_code=403,
            error_code="TENANT_MISMATCH",
            error_message="User does not belong to the correct tenant"
        )

    return user


def RoleChecker(allowed_roles: list[str]):
    def checker(user = Depends(get_current_user)):
        if user.role.name not in allowed_roles:
            raise AppException(
            status_code=403,
            error_code="UNAUTHORIZED",
            error_message="Unauthorized"
            )
        return user
    return checker
