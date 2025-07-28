import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel
from uuid import UUID

class RestaurantCreate(BaseModel):
    name: str
    address: Optional[str] = None
    restaurent_metadata: Optional[Dict] = None
    manager_ids: Optional[List[UUID]] = None  # Only used by SUPERADMIN
    is_active: Optional[bool] = True  # ✅ Added

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    restaurent_metadata: Optional[Dict] = None
    manager_ids: Optional[List[UUID]] = None  # Only used by SUPERADMIN

class RestaurantOut(BaseModel):
    id: UUID
    name: str
    address: Optional[str]
    restaurent_metadata: Optional[Dict]
    tenant_id: UUID
    is_active: bool  # ✅ Added
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class RestaurantResponse(BaseModel):
    id: UUID
    name: str
    address: Optional[str]
    restaurent_metadata: Optional[dict]
    tenant_id: UUID
    created_at: str
    created_by: UUID
    is_active: bool  # ✅ Added