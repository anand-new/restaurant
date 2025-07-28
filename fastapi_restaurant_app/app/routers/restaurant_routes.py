# app/routers/restaurant_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate, RestaurantOut
from app.db.engine import get_db
from app.middlewares.role_check import get_current_user
from app.services import restaurant_service

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

@router.post("/", response_model=RestaurantOut)
def create(data: RestaurantCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return restaurant_service.create_restaurant(db, data, user)

@router.get("/", response_model=list[RestaurantOut])
def list_all(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return restaurant_service.list_restaurants(db, user)

@router.get("/{restaurant_id}", response_model=RestaurantOut)
def get_one(restaurant_id: UUID, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return restaurant_service.get_restaurant(db, restaurant_id, user)

@router.put("/{restaurant_id}", response_model=RestaurantOut)
def update(restaurant_id: UUID, data: RestaurantUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return restaurant_service.update_restaurant(db, restaurant_id, data, user)

@router.delete("/{restaurant_id}")
def delete(restaurant_id: UUID, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return restaurant_service.delete_restaurant(db, restaurant_id, user)
