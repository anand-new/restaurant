# app/schemas/orders.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class OrderCreate(BaseModel):
    restaurant_id: UUID
    order_time: datetime
    menu_item: str
    quantity: int
    price: float
    weather_info: Optional[dict] = Field(default_factory=dict)
    external_factors: Optional[dict] = Field(default_factory=dict)
