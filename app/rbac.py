from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import verify_access_token
from app.models import AccessControl,UserPermission


def has_permission(resource: str, action: str):
    def checker(token_data: dict = Depends(verify_access_token), db: Session = Depends(get_db)):
        role = token_data.get("role")
        user_id = token_data.get("user_id")

        print(f"🔍 Checking permission for user: {user_id}, role: {role}, resource: {resource}, action: {action}")

        # Check user-specific permission
        user_perm = db.query(UserPermission).filter_by(
            user_id=user_id, resource=resource, action=action
        ).first()
        if user_perm:
            print("✅ Permission granted (user-specific)")
            return token_data

        # Fallback to role-based permission
        role_perm = db.query(AccessControl).filter_by(
            role=role, resource=resource, action=action
        ).first()
        if role_perm:
            print("✅ Permission granted (role-based)")
            return token_data

        print("❌ Permission denied")
        raise HTTPException(status_code=403, detail="Permission denied")
    return checker




# def has_permission(resource: str, action: str):
#     def checker(token_data: dict = Depends(verify_access_token), db: Session = Depends(get_db)):
#         role = token_data.get("role")
#         print("🔍 Role from token:", role)
#         permission = db.query(AccessControl).filter_by(
#             role=role, resource=resource, action=action
#         ).first()
#         if not permission:
#             raise HTTPException(status_code=403, detail="Permission denied")
#         return token_data
#     return checker
