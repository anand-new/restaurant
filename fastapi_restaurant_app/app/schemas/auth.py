from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
    email: str
    role: str
    isNew: bool
    tenant_id: UUID

class LoginRequest(BaseModel):
    username: str
    password: str

class FirstTimeResetRequest(BaseModel):
    old_password: str
    new_password: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class ForgotPasswordRequest(BaseModel):
    email: str

# For Forgot Password (requesting a reset link/token)
class PasswordResetRequest(BaseModel):
    email: EmailStr

# For Reset Password (after receiving token via email)
class PasswordResetConfirm(BaseModel):
    reset_token: str
    new_password: str = Field(..., min_length=8)

# For Logged-in Users Changing Their Password
class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)