from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, AccessControl
from app.auth import verify_access_token
from uuid import UUID

router = APIRouter()

@router.put("/users/promote/{user_id}")
def promote_user(user_id: UUID, new_role: str, db: Session = Depends(get_db), token_data: dict = Depends(verify_access_token)):
    current_role = token_data.get("role")
    
    permission = db.query(AccessControl).filter_by(
        role=current_role,
        resource="user",
        action="promote"
    ).first()

    if not permission:
        raise HTTPException(status_code=403, detail="You are not allowed to promote users")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = new_role
    db.commit()

    return {"message": f"User promoted to {new_role}"}
