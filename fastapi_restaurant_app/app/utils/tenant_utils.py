
from app.exceptions.http_exceptions import AppException

def assert_tenant_access(entity_tenant_id: str, current_user):
    if current_user.role.name != "superadmin" and entity_tenant_id != current_user.tenant_id:
        raise AppException(status_code=403,
                error_code="ACEESS_DENIED", error_message="Forbidden: tenant access denied")
