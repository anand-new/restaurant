from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.services.prediction_service import run_dummy_prediction
from app.middlewares.role_check import get_current_user
from app.db.deps import get_db  # ensures tenant-aware session

router = APIRouter()

@router.get("/")
def predict(
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    tenant_id = db.tenant_id
    if not tenant_id and user.role.name != "superadmin":
        return {"error": "Missing tenant context"}

    # Optionally scope restaurant_ids to tenant
    restaurant_ids = [
        ur.restaurant_id for ur in user.restaurants 
        if not tenant_id or ur.tenant_id == tenant_id  # Safety check if data is shared
    ]

    return run_dummy_prediction(restaurant_ids)
