from typing import List
from fastapi import HTTPException
from sqlalchemy import UUID
from sqlalchemy.orm import Session
from app.exceptions.http_exceptions import AppException
from app.models.role import Role
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserUpdate
from passlib.hash import pbkdf2_sha256 as hash
import uuid
from app.models.restaurant import Restaurant, UserRestaurant
from app.schemas.user import UserRestaurantDetailsResponse, UserWithRestaurants

from app.utils.tenant_utils import assert_tenant_access

def create_user(current_user, user_data: UserCreate, db: Session):
    # 🚫 Prevent users from creating users in other tenants (except superadmin)
    if current_user.role.name != "superadmin":
        if user_data.tenant_id != current_user.tenant_id:
            raise AppException(
                status_code=403,
                error_code="UNAUTHORIZED",
                error_message="You are not authorized to create users for other tenants."
            )

    # ✅ Ensure unique username and email within tenant
    existing_user = db.query(User).filter(
        User.username == user_data.username,
        User.tenant_id == user_data.tenant_id
    ).first()
    if existing_user:
        raise AppException(status_code=400,
                error_code="USERNAME_ALREADY_EXISTS", error_message="Username already exists for this tenant.")

    existing_email = db.query(User).filter(
        User.email == user_data.email,
        User.tenant_id == user_data.tenant_id
    ).first()
    if existing_email:
        raise AppException(status_code=400,
                error_code="EMAIL_ALREADY_EXISTS", error_message="Email already exists for this tenant.")

    role = db.query(Role).filter(Role.name == user_data.role).first()
    if not role:
        raise AppException(status_code=400,error_code="ROLE_DOES_NOT_EXIST", error_message=f"Role '{user_data.role}' not found")
    # 🔒 Create user with hashed password
    hashed_password = hash.hash(user_data.password)

    new_user = User(
        id=uuid.uuid4(),
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        tenant_id=user_data.tenant_id,
        role_id=role.id,
        created_by=current_user.id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": str(new_user.id),
        "username": new_user.username,
        "email": new_user.email,
        "tenant_id": str(new_user.tenant_id),
        "role": role.name
    }


def get_user_by_id(user_id: UUID, db: Session, user: User) -> User:
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise AppException(404, "USER_NOT_FOUND", "User not found")

    assert_tenant_access(target_user.tenant_id, user)
    return target_user


def update_user(user_id: UUID, payload: UserUpdate, db: Session, user: User) -> User:
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise AppException(404, "USER_NOT_FOUND", "User not found")

    assert_tenant_access(target_user.tenant_id, user)

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(target_user, field, value)

    db.commit()
    db.refresh(target_user)
    return target_user


def delete_user(user_id: UUID, db: Session, user: User):
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise AppException(404, "USER_NOT_FOUND", "User not found")

    assert_tenant_access(target_user.tenant_id, user)

    if not target_user.is_active:
        raise AppException(400, "USER_ALREADY_INACTIVE", "User is already deactivated")

    target_user.is_active = False
    db.commit()
    return {"message": "User deactivated successfully"}


def get_user_restaurant_summary(current_user: User, db: Session) -> UserRestaurantDetailsResponse:
    tenant_id = current_user.tenant_id

    if current_user.role.name == "superadmin":
        # All users in the same tenant
        users = db.query(User).filter(User.tenant_id == tenant_id, User.is_active == True).all()
        response = []

        for user in users:
            restaurant_ids = [
                ur.restaurant_id for ur in user.restaurants if ur.restaurant.is_active
            ]
            restaurants = db.query(Restaurant).filter(Restaurant.id.in_(restaurant_ids)).all()

            response.append(UserWithRestaurants(
                user_id=user.id,
                username=user.username,
                email=user.email,
                restaurants=restaurants
            ))

        return UserRestaurantDetailsResponse(users=response)

    else:
        # For non-superadmin: only their own mapped restaurants
        restaurant_ids = [
            ur.restaurant_id for ur in current_user.restaurants if ur.restaurant.is_active
        ]
        restaurants = db.query(Restaurant).filter(Restaurant.id.in_(restaurant_ids)).all()

        return UserRestaurantDetailsResponse(
            users=[
                UserWithRestaurants(
                    user_id=current_user.id,
                    username=current_user.username,
                    email=current_user.email,
                    restaurants=restaurants
                )
            ]
        )

def list_all_users_for_superadmin(current_user: User, db: Session) -> list[User]:
    if current_user.role.name.lower() != "superadmin":
        raise AppException(
            status_code=403,
            error_code="FORBIDDEN_ACCESS",
            error_message="Only superadmin can view all users"
        )

    users =  db.query(User).filter(User.tenant_id == current_user.tenant_id, User.is_active == True).all()
    user_out_list: List[UserOut] = [
    UserOut(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role.name if user.role else "N/A",
        is_active=user.is_active,
        created_at=user.created_at,
        tenant_id=user.tenant_id
    )
    for user in users
    ]
    return user_out_list