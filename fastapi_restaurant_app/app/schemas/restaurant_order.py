# app/schemas/restaurant_order.py
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class RestaurantOrderCreate(BaseModel):
    restaurant_id: int
    order_time: datetime
    menu_item: Optional[str]
    quantity: Optional[int]
    price: Optional[float]
    weather_info: Optional[Dict]
    external_factors: Optional[Dict]

class RestaurantOrderOut(RestaurantOrderCreate):
    id: int

    class Config:
        orm_mode = True
