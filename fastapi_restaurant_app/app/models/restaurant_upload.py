# app/models/restaurant_upload.py
import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.engine  import Base
from sqlalchemy.dialects.postgresql import UUID

class RestaurantUpload(Base):
    __tablename__ = "restaurant_uploads"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    upload_time = Column(DateTime(timezone=True), server_default=func.now())
    tenant_id = Column(UUID(as_uuid=True), nullable=False , default=uuid.uuid4)  # NEW
