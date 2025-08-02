from app.core.security import verify_password
from app.models.user import User
from app.exceptions.http_exceptions import AppException
from app.db.engine import SessionLocal
import uuid
import datetime
from passlib.hash import pbkdf2_sha256 as hash

from app.models.user import User
from app.schemas.auth import PasswordResetRequest, PasswordResetConfirm, PasswordChangeRequest
from app.exceptions.http_exceptions import AppException
from sqlalchemy.orm import Session
from sqlalchemy import or_

# def authenticate_user(username: str, password: str):
#     user = get_user_by_username(username)
#     if user and verify_password(password, user.password_hash):
#         return create_access_token({"sub": str(user.email), "tenant_id": user.tenant_id})
#     return None

# app/services/auth_service.py
def authenticate_user(username: str, password: str, db: Session):
    # db = SessionLocal()
    # user = db.query(User).filter(User.username == username).first()
    user = db.query(User).filter(
        or_(User.username == username, User.email == username)
    ).first()
    if not user:
        raise AppException(
            status_code=401,
            error_code="USER_NOT_FOUND",
            error_message="User with provided credentials does not exist"
        )
    if not verify_password(password, user.password_hash):
        raise AppException(
            status_code=401,
            error_code="INVALID_PASSWORD",
            error_message="Password is incorrect"
        )
    return user

def change_password(user: User, req: PasswordChangeRequest, db: Session):
    if not hash.verify(req.current_password, user.password_hash):
        raise AppException(status_code=400, error_code="INVALID_OLD_PASSWORD", error_message="Old password is incorrect")
    user.password_hash = hash.hash(req.new_password)
    user.is_new = False
    db.commit()
    return {"message": "Password changed successfully"}


def reset_password_first_time(user: User, new_password: str, db: Session):
    user.password_hash = hash.hash(new_password)
    user.is_new = False
    db.commit()
    return {"message": "Password reset successful"}


# --- FORGOT/RESET PASSWORD FLOW (token-based) ---

# In-memory store to simulate token store (you can use Redis or DB instead)
PASSWORD_RESET_TOKENS = {}

def initiate_forgot_password(req: PasswordResetRequest, db: Session):
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        raise AppException(status_code=404, error_code="USER_NOT_FOUND", error_message="User not found")
    
    token = str(uuid.uuid4())
    PASSWORD_RESET_TOKENS[token] = {
        "user_id": str(user.id),
        "expires_at": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }
    # TODO: Send email here with token
    return {"message": "Password reset token generated", "reset_token": token}


def confirm_reset_password(req: PasswordResetConfirm, db: Session):
    token_data = PASSWORD_RESET_TOKENS.get(req.reset_token)
    if not token_data or token_data["expires_at"] < datetime.datetime.utcnow():
        raise AppException(status_code=400, error_code="INVALID_TOKEN", error_message="Reset token is invalid or expired")

    user = db.query(User).filter(User.id == token_data["user_id"]).first()
    if not user:
        raise AppException(status_code=404, error_code="USER_NOT_FOUND", error_message="User not found")

    user.password_hash = hash.hash(req.new_password)
    user.is_new = False
    db.commit()

    del PASSWORD_RESET_TOKENS[req.reset_token]
    return {"message": "Password reset successful"}


# --- LOGOUT PLACEHOLDER (JWT blacklist if needed) ---

def logout_user(token: str):
    # TODO: Add token to blacklist store (e.g., Redis)
    return {"message": "User logged out successfully"}
