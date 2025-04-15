from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User,AccessControl
from app.auth import encrypt_password, decrypt_password, create_access_token
from pydantic import BaseModel, EmailStr
import uuid
from uuid import UUID
from app.rbac import has_permission

router = APIRouter()

class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AccessRequest(BaseModel):
    role: str
    resource: str
    action: str
class AccessResponse(BaseModel):
    id:UUID
    role: str
    resource: str
    action: str

class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True

# 📌 User Signup (Default role: 'member')
@router.post("/signup", status_code=201)
def signup(user_data: SignupRequest, db: Session = Depends(get_db)):
    # Check for existing email
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    # Encrypt password
    encrypted_pass = encrypt_password(user_data.password)

    # Create new user with role 'member'
    new_user = User(
        id=uuid.uuid4(),
        username=user_data.username,
        email=user_data.email,
        password_encrypted=encrypted_pass,
        role="member"  # Default role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully. Default role: member"}

# 📌 User Login (All roles)
@router.post("/login")
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verify password
    try:
        decrypted_pass = decrypt_password(user.password_encrypted)
        if decrypted_pass != credentials.password:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception:
        raise HTTPException(status_code=401, detail="Error verifying password")

    # Generate JWT token
    token = create_access_token({
        "sub": user.email,
        "role": user.role,
        "user_id": str(user.id)
    })

    return {"access_token": token,"role":user.role, "token_type": "bearer"}


@router.get("/get_users/", response_model=List[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    user=Depends(has_permission("user", "read"))
):
    return db.query(User).all()
###Access Lists
@router.get("/access_list/",response_model=List[AccessResponse])
def get_all_access(db: Session = Depends(get_db), user=Depends(has_permission("access", "read"))):
    return db.query(AccessControl).all()


@router.post("/add_access/", response_model=AccessResponse, status_code=201)
def add_acess(Access_data: AccessRequest, db: Session = Depends(get_db), user=Depends(has_permission("access", "add"))):
    new_access = AccessControl(
        id=uuid.uuid4(),
        role=Access_data.role,
        resource=Access_data.resource,
        action=Access_data.action
        
    )
    db.add(new_access)
    db.commit()
    db.refresh(new_access)
    return new_access

@router.put("/update_access/{id}", response_model=AccessResponse)
def update_access(access_id: str, access_data: AccessRequest, db: Session = Depends(get_db), user=Depends(has_permission("access", "update"))):
    access = db.query(AccessControl).filter(AccessControl.id == uuid.UUID(access_id)).first()
    if not access:
        raise HTTPException(status_code=404, detail="access id not found")
    access.role = access_data.role
    access.resource = access_data.resource
    access.action = access_data.action
    db.commit()
    db.refresh(access)
    return access