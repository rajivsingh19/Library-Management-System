from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, String, Boolean, UUID
import uuid
from .database import Base
from sqlalchemy.orm import relationship

class Admin(Base):
    __tablename__ = "admin"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_encrypted = Column(String)  # Storing encrypted password
    role = Column(String, default="librarian")  # "admin"
    is_active = Column(Boolean, default=True)

# 📌 Library Member Model
class Member(Base):
    __tablename__ = "members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_encrypted = Column(String)  # Storing encrypted password
    role = Column(String, default="member")  # Explicitly setting role
    is_active = Column(Boolean, default=True)

    # Relationships
    borrowings = relationship("Borrowing", back_populates="member")

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
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)
    borrowed_at = Column(DateTime, default=datetime.utcnow)
    returned_at = Column(DateTime, nullable=True)

    # Relationships
    member = relationship("Member", back_populates="borrowings")
    book = relationship("Book", back_populates="borrowings")

