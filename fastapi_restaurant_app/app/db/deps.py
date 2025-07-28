from fastapi import Depends, Request
from sqlalchemy.orm import Session
from app.db.engine import SessionLocal

def get_db(request: Request):
    db: Session = SessionLocal()
    try:
        if hasattr(request.state, "tenant_id") and request.state.tenant_id:
            db.tenant_id = request.state.tenant_id
        else:
            db.tenant_id = None
        yield db
    finally:
        db.close()