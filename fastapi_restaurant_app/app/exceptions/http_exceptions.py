# app/exceptions/http_exceptions.py

from fastapi import HTTPException

class AppException(HTTPException):
    def __init__(self, status_code: int, error_code: str, error_message: str):
        detail = {
            "error_code": error_code,
            "error_message": error_message
        }
        super().__init__(status_code=status_code, detail=detail)
