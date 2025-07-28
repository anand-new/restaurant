from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from app.exceptions.http_exceptions import AppException
from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate
from app.middlewares.role_check import get_current_user
from app.db.deps import get_db

router = APIRouter()

@router.post("/")
def create_tenant(tenant: TenantCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role.name != "superadmin":
        raise AppException(
            status_code=403,
            error_code="ONLY_SUPERADMIN_CAN_CREATE_TENANTS",
            error_message="Only superadmin can create tenants"
            )

    if db.query(Tenant).filter(Tenant.name == tenant.name).first():
        raise AppException(
            status_code=400,
            error_code="TENANT_NAME_ALREADY_EXISTS",
            error_message="Tenant name already exists"
            )

    new_tenant = Tenant(id=uuid4(), name=tenant.name)
    db.add(new_tenant)
    db.commit()
    db.refresh(new_tenant)
    return {"id": str(new_tenant.id), "name": new_tenant.name}
