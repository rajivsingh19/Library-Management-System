from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Borrowing, Book
from app.auth import decrypt_password, verify_access_token,encrypt_password


router = APIRouter()

# 👤 Member: View Own Profile
@router.get("/get_my_profile")
def get_my_profile(token_data: dict = Depends(verify_access_token), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=token_data["user_id"]).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "username": user.username,
        "email": user.email,
        "role": user.role
    }

# 📚 Member: View Borrowed Books
@router.get("/get_borrowed_books")
def get_borrowed_books(token_data: dict = Depends(verify_access_token), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=token_data["user_id"]).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    borrowings = db.query(Borrowing).filter_by(user_id=user.id).all()

    borrowed_books = []
    for b in borrowings:
        book = db.query(Book).filter_by(id=b.book_id).first()
        borrowed_books.append({
            "book_id": str(book.id),
            "title": book.title,
            "author": book.author,
            "isbn": book.isbn,
            "borrowed_at": b.borrowed_at,
            "returned_at": b.returned_at
        })

    return {"borrowed_books": borrowed_books}

# 👤 Member: Update Own Profile
class UpdateUserProfile(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
@router.put("/update_profile")
def update_profile(updated_user: UpdateUserProfile, token_data: dict = Depends(verify_access_token), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=token_data["user_id"]).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Only allow update to the username and email for now
    user.username = updated_user.username or user.username
    user.email = updated_user.email or user.email

    db.commit()

    return {
        "message": "Profile updated successfully",
        "username": user.username,
        "email": user.email
    }
@router.put("/password")
def update_password(old_password: str, new_password: str, token_data: dict = Depends(verify_access_token), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=token_data["user_id"]).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Decrypt the stored password and verify the old password
    decrypted_password = decrypt_password(user.password_encrypted)  # assuming 'user.password' holds the encrypted password

    if decrypted_password != old_password:
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    # Hash the new password before saving it
    user.password_encrypted = encrypt_password(new_password)

    db.commit()

    return {
        "message": "Password updated successfully"
    }