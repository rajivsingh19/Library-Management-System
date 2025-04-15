from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, String, Boolean, UUID
import uuid
from .database import Base
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_encrypted = Column(String, nullable=False)
    role = Column(String, default="member")  # Can be "admin" or "member"
    is_active = Column(Boolean, default=True)

class AccessControl(Base):
    __tablename__ = "access_control"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role = Column(String, nullable=False)
    resource = Column(String, nullable=False)  # e.g., "book"
    action = Column(String, nullable=False)    # e.g., "create", "read", "update", "delete"
   
class UserPermission(Base):
    __tablename__ = "user_permissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    resource = Column(String, nullable=False)
    action = Column(String, nullable=False)
# 📌 Book Model
class Book(Base):
    __tablename__ = "books"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    is_available = Column(Boolean, default=True)
    # Relationship
    borrowings = relationship("Borrowing", back_populates="book")

# 📌 Borrowing Model (Tracks which members borrowed which books)
class Borrowing(Base):
    __tablename__ = "borrowings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)
    borrowed_at = Column(DateTime, default=datetime.utcnow)
    is_return_requested = Column(Boolean, default=False) 
    returned_at = Column(DateTime, nullable=True)
    book = relationship("Book", back_populates="borrowings")

