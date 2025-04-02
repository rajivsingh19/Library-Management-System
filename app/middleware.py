from fastapi import HTTPException, Depends
from app.auth import verify_access_token

def librarian_required(token_data: dict = Depends(verify_access_token)):
    if token_data.get("role") != "librarian":
        raise HTTPException(status_code=403, detail="Access forbidden: Librarian role required")
    return token_data
