# app/services/restaurant_service.py

from sqlalchemy import UUID
from app.models.restaurant import Restaurant, UserRestaurant
from app.models.user import User
from app.exceptions.http_exceptions import AppException
from sqlalchemy.orm import Session
from app.utils.tenant_utils import assert_tenant_access
import uuid

def create_restaurant(db: Session, data, user):
    restaurant = Restaurant(
        name=data.name,
        address=data.address,
        restaurent_metadata=data.restaurent_metadata,
        tenant_id=user.tenant_id,
        created_by=user.id
    )
    db.add(restaurant)
    db.flush()

    # Only SUPERADMIN can assign managers
    if data.manager_ids and user.role.name == "SUPERADMIN":
        for manager_id in data.manager_ids:
            db.add(UserRestaurant(user_id=manager_id, restaurant_id=restaurant.id))

    db.commit()
    db.refresh(restaurant)
    return restaurant

def update_restaurant(db: Session, restaurant_id: uuid.UUID, data, user):
    restaurant = db.query(Restaurant).filter_by(id=restaurant_id).first()
    if not restaurant:
        raise AppException(404, "RESTAURANT_NOT_FOUND", "Restaurant not found")
    
    assert_tenant_access(restaurant.tenant_id, user)

    if data.name: restaurant.name = data.name
    if data.address: restaurant.address = data.address
    if data.restaurent_metadata is not None:
        restaurant.restaurent_metadata = data.restaurent_metadata

    if data.manager_ids is not None:
        if user.role.name != "SUPERADMIN":
            raise AppException(403, "FORBIDDEN", "Only SUPERADMIN can assign managers")
        db.query(UserRestaurant).filter_by(restaurant_id=restaurant.id).delete()
        for manager_id in data.manager_ids:
            db.add(UserRestaurant(user_id=manager_id, restaurant_id=restaurant.id))

    db.commit()
    db.refresh(restaurant)
    return restaurant

def get_restaurant(db: Session, restaurant_id: uuid.UUID, user):
    restaurant = db.query(Restaurant).filter_by(id=restaurant_id).first()
    if not restaurant:
        raise AppException(404, "RESTAURANT_NOT_FOUND", "Restaurant not found")
    
    assert_tenant_access(restaurant.tenant_id, user)
    return restaurant

def delete_restaurant(restaurant_id: UUID, db: Session, user: User):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

    if not restaurant:
        raise AppException(
            status_code=404,
            error_code="RESTAURANT_NOT_FOUND",
            error_message="Restaurant not found."
        )

    # Enforce tenant isolation
    assert_tenant_access(restaurant.tenant_id, user)

    if not restaurant.is_active:
        raise AppException(
            status_code=400,
            error_code="RESTAURANT_ALREADY_INACTIVE",
            error_message="Restaurant is already marked as inactive."
        )

    # Soft delete
    restaurant.is_active = False
    db.commit()

    return {"message": "Restaurant deactivated successfully"}

def list_restaurants(db: Session, user):
    # SUPERADMIN can view all restaurants in their tenant
    # Others see only restaurants they manage
    if user.role.name.lower() == "superadmin":
        return db.query(Restaurant).all()

    return (
        db.query(Restaurant)
        .join(UserRestaurant, UserRestaurant.restaurant_id == Restaurant.id)
        .filter(UserRestaurant.user_id == user.id)
        .all()
    )
