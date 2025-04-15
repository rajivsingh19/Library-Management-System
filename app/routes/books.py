from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Book
from pydantic import BaseModel
from typing import List
from uuid import UUID
import uuid
# from app.auth import verify_access_token
from app.rbac import has_permission

router = APIRouter()

class BookRequest(BaseModel):
    title: str
    author: str
    isbn: str

    class Config:
        schema_extra = {
            "example": {
                "title": "The Alchemist",
                "author": "Paulo Coelho",
                "isbn": "9780061122415"
            }
        }

class BookResponse(BaseModel):
    id: UUID
    title: str
    author: str
    isbn: str
    is_available: bool

    class Config:
        from_attributes = True

@router.get("/books_list/",response_model=List[BookResponse])
def get_all_books(db: Session = Depends(get_db), user=Depends(has_permission("book", "read"))):
    return db.query(Book).all()

@router.post("/add_book/", response_model=BookResponse, status_code=201)
def add_book(book_data: BookRequest, db: Session = Depends(get_db), user=Depends(has_permission("book", "create"))):
    new_book = Book(
        id=uuid.uuid4(),
        title=book_data.title,
        author=book_data.author,
        isbn=book_data.isbn,
        is_available=True
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.put("/update_book/{book_id}", response_model=BookResponse)
def update_book(book_id: str, book_data: BookRequest, db: Session = Depends(get_db), user=Depends(has_permission("book", "update"))):
    book = db.query(Book).filter(Book.id == uuid.UUID(book_id)).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.title = book_data.title
    book.author = book_data.author
    book.isbn = book_data.isbn
    db.commit()
    db.refresh(book)
    return book

@router.delete("/delete_books/{book_id}")
def delete_book(book_id: str, db: Session = Depends(get_db), user=Depends(has_permission("book", "delete"))):
    book = db.query(Book).filter(Book.id == uuid.UUID(book_id)).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted"}











