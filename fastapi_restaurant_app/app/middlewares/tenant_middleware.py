# --- Step 2: Middleware to extract tenant_id from JWT ---
# File: app/middleware/tenant_middleware.py

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt
from app.config import JWT_SECRET_KEY, JWT_ALGORITHM

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        if token and token.startswith("Bearer "):
            try:
                payload = jwt.decode(token[7:], JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
                request.state.tenant_id = payload.get("tenant_id")
            except JWTError:
                return JSONResponse(status_code=401, content={"detail": "Invalid token"})
        else:
            request.state.tenant_id = None

        return await call_next(request)