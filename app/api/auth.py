from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.db.session import get_db
import bcrypt

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(request: LoginRequest, db=Depends(get_db)):
    user = await db.user.find_unique(where={"email": request.email})
    if not user or not bcrypt.checkpw(request.password.encode("utf-8"), user.password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {
        "message": f"Login successful! Redirect to {user['role'].lower()} dashboard.",
        "role": user["role"]
    }
