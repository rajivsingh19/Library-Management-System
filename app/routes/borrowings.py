
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import Book, Borrowing,User
from app.rbac import has_permission
import uuid

router = APIRouter()

# 📌 Borrow a book
@router.post("/borrow_book/{book_id}")
def borrow_book(book_id: str,
                token_data: dict = Depends(has_permission("book", "read")),
                db: Session = Depends(get_db)):

    book = db.query(Book).filter_by(id=book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if not book.is_available:
        raise HTTPException(status_code=400, detail="Book is already borrowed")

    borrowing = Borrowing(
        id=uuid.uuid4(),
        user_id=token_data["user_id"],
        book_id=book.id,
        borrowed_at=datetime.utcnow()
    )

    book.is_available = False  # Mark book as borrowed
    db.add(borrowing)
    db.commit()

    return {"message": f"You have borrowed '{book.title}'"}


# 📌 Return a book
# @router.post("/return_book/{book_id}")
# def return_book(book_id: str,
#                 token_data: dict = Depends(has_permission("book", "return")),
#                 db: Session = Depends(get_db)):

#     borrowing = db.query(Borrowing).filter_by(
#         book_id=book_id,
#         user_id=token_data["user_id"],
#         returned_at=None
#     ).first()

#     if not borrowing:
#         raise HTTPException(status_code=404, detail="No active borrowing found for this book")

#     borrowing.returned_at = datetime.utcnow()

#     book = db.query(Book).filter_by(id=book_id).first()
#     if book:
#         book.is_available = True  # Mark as available

#     db.commit()

#     return {"message": f"You have returned '{book.title}'"}
@router.post("/return_book/{book_id}")
def return_book_request(book_id: str,
                        token_data: dict = Depends(has_permission("book", "return")),
                        db: Session = Depends(get_db)):

    borrowing = db.query(Borrowing).filter_by(
        book_id=book_id,
        user_id=token_data["user_id"],
        returned_at=None
    ).first()

    if not borrowing:
        raise HTTPException(status_code=404, detail="No active borrowing found for this book")

    if borrowing.is_return_requested:
        raise HTTPException(status_code=400, detail="Return request already sent.")

    borrowing.is_return_requested = True
    db.commit()

    return {"message": f"Return request for '{borrowing.book.title}' submitted. Pending approval."}
@router.post("/approve_return/{borrowing_id}")
def approve_return(borrowing_id: str,
                   token_data: dict = Depends(has_permission("borrowing", "update")),
                   db: Session = Depends(get_db)):

    borrowing = db.query(Borrowing).filter_by(id=borrowing_id).first()

    if not borrowing or borrowing.returned_at is not None:
        raise HTTPException(status_code=404, detail="Invalid or already returned.")

    if not borrowing.is_return_requested:
        raise HTTPException(status_code=400, detail="No return request found.")

    borrowing.returned_at = datetime.utcnow()
    borrowing.is_return_requested = False

    book = db.query(Book).filter_by(id=borrowing.book_id).first()
    if book:
        book.is_available = True

    db.commit()

    return {"message": f"Return for book '{book.title}' approved."}


# @router.get("/all_borrowed_books/")
# def get_all_borrowed_books(token_data: dict = Depends(has_permission("borrowing", "read")),
#                            db: Session = Depends(get_db)):
#     borrowings = db.query(Borrowing).all()

#     result = []
#     for b in borrowings:
#         book = db.query(Book).filter_by(id=b.book_id).first()
#         user = db.query(User).filter_by(id=b.user_id).first()

#         result.append({
#             "book_id": book.id,
#             "book_title": book.title,
#             "book_author": book.author,
#             "isbn": book.isbn,
#             "borrowed_by": user.username,
#             "user_email": user.email,
#             "borrowed_at": b.borrowed_at,
#             "returned_at": b.returned_at
#         })

#     return {"total": len(result), "borrowed_books": result}

@router.get("/all_borrowed_books/")
def get_all_borrowed_books(token_data: dict = Depends(has_permission("borrowing", "read")),
                           db: Session = Depends(get_db)):

    role = token_data.get("role")
    user_id = token_data.get("user_id")

    # 🧠 If member: show only their borrowed books
    if role == "member":
        borrowings = db.query(Borrowing).filter_by(user_id=user_id).all()
    else:
        # 🧠 If librarian/admin: show all borrowings
        borrowings = db.query(Borrowing).all()

    result = []
    for b in borrowings:
        book = db.query(Book).filter_by(id=b.book_id).first()
        user = db.query(User).filter_by(id=b.user_id).first()

        result.append({
            "borrowing_id": b.id,
            "book_id": book.id,
            "book_title": book.title,
            "book_author": book.author,
            "isbn": book.isbn,
            "borrowed_by": user.username,
            "user_email": user.email,
            "borrowed_at": b.borrowed_at,
            "returned_at": b.returned_at,
            "return_requested": getattr(b, "is_return_requested", False)  # fallback for safety
        })

    return {"total": len(result), "borrowed_books": result}
