from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import engine, Base
from app.models import *

# Import your routers
from app.routers import auth_routes, orders_routes, prediction_routes,restaurant_upload_routes,user_routes
from app.routers import orders_routes


from app.middlewares.tenant_middleware import TenantMiddleware

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.schemas.error import ErrorResponse
from app.exceptions.http_exceptions import AppException

# Initialize FastAPI
app = FastAPI(
    title="Restaurant Demand Prediction API",
    description="Supports multi-tenancy, role-based access, uploads, and demand prediction data.",
    version="1.0.0"
)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error_code": "INTERNAL_SERVER_ERROR",
            "error_message": "An unexpected error occurred"
        }
    )

# CORS middleware (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(TenantMiddleware)

# Create DB tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(restaurant_upload_routes.router, prefix="/restaurants", tags=["Restaurants"])
# app.include_router(uploads.router, prefix="/upload", tags=["Uploads"])
app.include_router(orders_routes.router, prefix="/orders", tags=["Orders"])
app.include_router(prediction_routes.router, prefix="/predict", tags=["Prediction"])

# Health check
@app.get("/", tags=["Health"])
def read_root():
    return {"message": "API is up and running 🚀"}
