import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.db.engine  import Base

class RestaurantOrder(Base):
    __tablename__ = "restaurant_orders"
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurants.id"))
    order_time = Column(TIMESTAMP, nullable=False)
    menu_item = Column(String)
    quantity = Column(Integer)
    price = Column(Integer)
    weather_info = Column(JSON)
    external_factors = Column(JSON)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)  # NEW