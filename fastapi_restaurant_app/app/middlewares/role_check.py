from fastapi import Depends, HTTPException, status
from app.core.jwt import decode_token
from fastapi.security import OAuth2PasswordBearer
from app.exceptions.http_exceptions import AppException
from app.services.user_service import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise AppException(
            status_code=401,
            error_code="INVALID_TOKEN",
            error_message="Invalid token"
        )
    user = get_user_by_id(payload.get("sub"))
    if user is None:
        raise AppException(
            status_code=404,
            error_code="USER_NOT_FOUND",
            error_message="User not found"
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
