from fastapi import APIRouter, Depends, Body, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.auth import Token, PasswordResetRequest, PasswordResetConfirm, PasswordChangeRequest
from app.services.auth_service import (
    authenticate_user,
    logout_user,
    initiate_forgot_password,
    confirm_reset_password,
    reset_password_first_time,
    change_password
)
from app.middlewares.role_check import get_current_user
from app.exceptions.http_exceptions import AppException
from app.core.jwt import create_access_token
from app.db.deps import get_db

router = APIRouter()


@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise AppException(status_code=401, error_code="INVALID_CREDENTIALS", error_message="Invalid credentials")

    access_token = create_access_token({
        "sub": user.username,
        "user_id": str(user.id),
        "tenant_id": str(user.tenant_id),
        "role": user.role.name
    })

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
        "email": user.email,
        "tenant_id": str(user.tenant_id)
    }


@router.post("/logout")
def logout(user=Depends(get_current_user)):
    logout_user("dummy_token")  # You can update this with real token handling logic
    return {"message": "Logout successful"}


@router.post("/forgot-password")
def forgot_password(data: PasswordResetRequest, db: Session = Depends(get_db)):
    return initiate_forgot_password(data, db)


@router.post("/reset-password")
def reset_password(data: PasswordResetConfirm, db: Session = Depends(get_db)):
    return confirm_reset_password(data, db)


@router.post("/reset-initial-password")
def reset_initial_password_endpoint(password: str = Body(...), db: Session = Depends(get_db), user=Depends(get_current_user)):
    return reset_password_first_time(user, password, db)


@router.post("/change-password")
def change_password_endpoint(data: PasswordChangeRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return change_password(user, data, db)
