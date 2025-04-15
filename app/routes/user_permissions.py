from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User, UserPermission
from app.database import get_db
from app.auth import verify_access_token
from app.rbac import has_permission
import uuid

router = APIRouter()


@router.post("/add_user_permissions/")
def add_user_permission(
    user_id: uuid.UUID,
    resource: str,
    action: str,
    db: Session = Depends(get_db),
    token_data: dict = Depends(has_permission("user_permission", "add"))
):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing = db.query(UserPermission).filter_by(user_id=user_id, resource=resource, action=action).first()
    if existing:
        raise HTTPException(status_code=400, detail="Permission already exists for user")

    perm = UserPermission(user_id=user_id, resource=resource, action=action)
    db.add(perm)
    db.commit()
    return {"message": "User-specific permission added"}


@router.get("/get_user_permissions/")
def get_all_user_permissions(
    db: Session = Depends(get_db),
    token_data: dict = Depends(has_permission("user_permission", "read"))
):
    return db.query(UserPermission).all()


@router.delete("/delete_user_permissions/")
def delete_user_permission(
    user_id: uuid.UUID,
    resource: str,
    action: str,
    db: Session = Depends(get_db),
    token_data: dict = Depends(has_permission("user_permission", "delete"))
):
    perm = db.query(UserPermission).filter_by(user_id=user_id, resource=resource, action=action).first()
    if not perm:
        raise HTTPException(status_code=404, detail="Permission not found")

    db.delete(perm)
    db.commit()
    return {"message": "User-specific permission removed"}
