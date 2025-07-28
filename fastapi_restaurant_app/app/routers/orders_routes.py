from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request
from sqlalchemy.orm import Session
from datetime import datetime
import csv, io, json

from app.db.deps import get_db  # tenant-aware
from app.exceptions.http_exceptions import AppException
from app.models.restaurant_order import RestaurantOrder
from app.schemas.orders import OrderCreate
from app.middlewares.role_check import get_current_user
from app.models.restaurant import Restaurant
from app.utils.tenant_utils import assert_tenant_access

router = APIRouter()

# POST /orders - Submit a new order

@router.post("/", summary="Submit a new restaurant order")
def submit_order(
    request: Request,
    order: OrderCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    tenant_id = db.tenant_id

    # 🧠 Validate restaurant belongs to tenant
    restaurant = db.query(Restaurant).filter(Restaurant.id == order.restaurant_id).first()
    if not restaurant:
        raise AppException(
            status_code=404,
            error_code="RESTAURANT_NOT_FOUND",
            error_message="Restaurant not found"
            )

    assert_tenant_access(restaurant.tenant_id, user)

    db_order = RestaurantOrder(
        restaurant_id=order.restaurant_id,
        order_time=order.order_time,
        menu_item=order.menu_item,
        quantity=order.quantity,
        price=order.price,
        weather_info=order.weather_info,
        external_factors=order.external_factors,
        tenant_id=tenant_id
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return {"message": "Order submitted successfully", "order_id": db_order.id}



# POST /predict - Accept restaurant_id and date range for demand prediction PoC
@router.post("/predict", summary="Run demand prediction (PoC)")
def predict_demand(
    restaurant_id: str,
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise AppException(
            status_code=404,
            error_code="RESTAURANT_NOT_FOUND",
            error_message="Restaurant not found"
            )

    assert_tenant_access(restaurant.tenant_id, user)

    return {
        "restaurant_id": restaurant_id,
        "start_date": start_date,
        "end_date": end_date,
        "predicted_demand": [
            {"date": start_date, "menu_item": "Burger", "predicted_qty": 120},
            {"date": end_date, "menu_item": "Pizza", "predicted_qty": 80},
        ]
    }

