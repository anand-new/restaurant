from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.exceptions.http_exceptions import AppException
from app.utils.csv_loader import parse_and_create_restaurants
from app.middlewares.role_check import get_current_user, RoleChecker
from app.db.deps import get_db  # ✅ use tenant-aware DB session
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/upload", dependencies=[Depends(RoleChecker(["ADMIN"]))])
async def upload_csv(
    file: UploadFile = File(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # ✅ Enforce tenant access
    if not db.tenant_id:
        raise AppException(
            status_code=400,
            error_code="TENANT_ID_NOT_FOUND_IN_TOKEN",
            error_message="Tenant ID not found in token"
            )

    restaurants = parse_and_create_restaurants(file.file, db, user.id, tenant_id=db.tenant_id)

    return {"created": len(restaurants)}

