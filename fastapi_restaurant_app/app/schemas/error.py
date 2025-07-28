# app/schemas/error.py

from pydantic import BaseModel

class ErrorResponse(BaseModel):
    error_code: str
    error_message: str
