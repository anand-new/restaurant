# app/schemas/user.py
import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from app.schemas.restaurant import RestaurantOut

class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str
    tenant_id: Optional[UUID] = None  # <-- add this
    is_active: Optional[bool] = True


class UserUpdate(BaseModel):
    full_name: Optional[str]
    email: Optional[EmailStr]
    role: Optional[str]  # Only editable by SUPERADMIN logic if needed

class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    full_name: Optional[str]
    role: str
    is_active: bool
    # tenant_id: UUID

    class Config:
        from_attributes = True


class UserWithRestaurants(BaseModel):
    user_id: UUID
    username: str
    email: EmailStr
    restaurants: List[RestaurantOut]

class UserRestaurantDetailsResponse(BaseModel):
    users: List[UserWithRestaurants]

class UserOut(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime.datetime
    tenant_id: Optional[UUID] = None 

    class Config:
        orm_mode = True