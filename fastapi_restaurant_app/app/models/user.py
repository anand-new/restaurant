import datetime
from sqlalchemy import TIMESTAMP, Boolean, Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.engine import Base

# class User(Base):
#     __tablename__ = "users"
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     username = Column(String, unique=True, nullable=False)
#     email = Column(String, unique=True, nullable=False)
#     password_hash = Column(String, nullable=False)
#     role_id = Column(Integer, ForeignKey("roles.id"))
#     created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

#     role = relationship("Role")
#     restaurants = relationship("UserRestaurant", back_populates="user")

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)  # NEW
    force_password_reset = Column(Boolean, default=True) 
    is_active = Column(Boolean, default=True)

    role = relationship("Role")
    restaurants = relationship("UserRestaurant", back_populates="user")