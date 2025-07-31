from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.exceptions.http_exceptions import AppException
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.services.user_service import create_user, list_all_users_for_superadmin
from app.middlewares.role_check import get_current_user
from app.db.deps import get_db
from app.schemas.user import UserUpdate, UserResponse
from app.services.user_service import update_user, get_user_by_id, delete_user
from app.middlewares.role_check import get_current_user, RoleChecker

router = APIRouter()

@router.post("/")
def create_user_route(
    user_data: UserCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    tenant_id = request.state.tenant_id
    user_role = current_user.role.name

    # 🛡️ Only superadmin can assign other tenant_id
    if user_data.tenant_id and user_role != "superadmin":
        raise AppException(
            status_code=403,
            error_code="ONLY_SUPERADMIN_CAN_ASSIGN_TENANT_ID_EXPLICITLY",
            error_message="Only superadmin can assign tenant_id explicitly"
            )

    # 🏢 Auto-assign tenant_id from token if not provided
    if not user_data.tenant_id:
        if not tenant_id:
            raise AppException(
                    status_code=400,
                    error_code="TENANT_ID_MISSING_FROM_REQUEST",
                    error_message="Tenant ID missing from request"
                  )
        user_data.tenant_id = tenant_id

    return create_user(current_user, user_data, db)


# GET /users/{user_id} - Read user details
@router.get("/{user_id}", response_model=UserResponse,  dependencies=[Depends(RoleChecker(["admin", "superadmin"]))])
def read_user(user_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_user_by_id(user_id=user_id, db=db, user=current_user)


# # # PUT /users/{user_id} - Update user
@router.put("/{user_id}", response_model=UserResponse, dependencies=[Depends(RoleChecker(["admin", "superadmin"]))])
def update_user_details(user_id: UUID, payload: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_user(user_id=user_id, payload=payload, db=db, user=current_user)


# # DELETE /users/{user_id} - Soft delete user
@router.delete("/{user_id}", summary="Deactivate user", dependencies=[Depends(RoleChecker(["admin", "superadmin"]))])
def deactivate_user(user_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_user(user_id=user_id, db=db, user=current_user)



@router.get("/", response_model=list[UserOut])
def list_users(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return list_all_users_for_superadmin(current_user, db)


# @router.get("/superadmin/users", response_model=list[UserResponse], dependencies=[Depends(RoleChecker(["SUPERADMIN"]))])
# def list_users_for_superadmin(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     return list_all_users_for_superadmin(current_user=current_user, db=db)