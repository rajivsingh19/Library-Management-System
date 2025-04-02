from fastapi import FastAPI
from app.database import engine, Base
from app.routes import  librarian

# Initialize FastAPI App
app = FastAPI(title="Library Book Management System", version="1.0")

# Create Database Tables
Base.metadata.create_all(bind=engine)

# Include Routes
# app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(librarian.router, prefix="/librarian", tags=["Librarian"])
# app.include_router(admin.router, prefix="/admin", tags=["Admin"])
# app.include_router(books.router, prefix="/books", tags=["Books"])
# app.include_router(users.router, prefix="/users", tags=["Users"])

# Root Endpoint
@app.get("/")
def home():
    return {"message": "Welcome to Library Book Management System"}

