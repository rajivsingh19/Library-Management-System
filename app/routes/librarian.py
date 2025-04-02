from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Admin
from app.auth import encrypt_password, decrypt_password, create_access_token
from pydantic import BaseModel

router = APIRouter()

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/librarian/signup")
def librarian_signup(user_data: SignupRequest, db: Session = Depends(get_db)):
    existing_user = db.query(Admin).filter(Admin.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    encrypted_pass = encrypt_password(user_data.password)
    
    new_librarian = Admin(
        username=user_data.username,
        email=user_data.email,
        password_encrypted=encrypted_pass,
        role="librarian"
    )
    db.add(new_librarian)
    db.commit()
    return {"message": "Librarian registered successfully"}

@router.post("/librarian/login")
def librarian_login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Admin).filter(Admin.email == credentials.email).first()
    if not user or user.role != "librarian":
        raise HTTPException(status_code=401, detail="Invalid credentials or not a librarian")

    decrypted_pass = decrypt_password(user.password_encrypted)
    
    if decrypted_pass != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
