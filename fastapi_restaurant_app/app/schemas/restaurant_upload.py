# app/schemas/restaurant_upload.py
from pydantic import BaseModel
from datetime import datetime

class RestaurantUploadCreate(BaseModel):
    file_name: str
    file_path: str
    uploaded_by: int
    restaurant_id: int

class RestaurantUploadOut(RestaurantUploadCreate):
    id: int
    upload_time: datetime

    class Config:
        orm_mode = True
