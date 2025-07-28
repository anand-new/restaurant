from sqlalchemy import Boolean, Column, String, ForeignKey, JSON, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.engine import Base
import uuid
import datetime

class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    address = Column(String)
    restaurent_metadata = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    tenant_id = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)  # NEW
    is_active = Column(Boolean, default=True)

    managers = relationship("UserRestaurant", back_populates="restaurant")



class UserRestaurant(Base):
    __tablename__ = "user_restaurants"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurants.id"), primary_key=True)

    user = relationship("User", back_populates="restaurants")
    restaurant = relationship("Restaurant", back_populates="managers")
