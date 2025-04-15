from fastapi import FastAPI
from app.database import engine, Base
from app.routes import books,users,promote,borrowings,profile,user_permissions
from app.initial_setup import create_default_admin_and_permissions


app = FastAPI(title="Library Book Management System", version="1.0")

# Create Database Tables
Base.metadata.create_all(bind=engine)

# Initialize admin and permissions
create_default_admin_and_permissions()

# Include Routes
app.include_router(promote.router, prefix="/promote", tags=["Promote"])
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(borrowings.router, prefix="/borrowings", tags=["Borrowings"])
app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(user_permissions.router)



# Root Endpoint
@app.get("/")
def home():
    return {"message": "Welcome to Library Book Management System"}

