from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.db.crud import get_user_by_email, create_user
from app.db.session import get_db
import bcrypt

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    phone: str = None
    city: str
    state: str
    country: str
    role: str


@router.post("/login")
async def login(request: LoginRequest, db=Depends(get_db)):
    user = await get_user_by_email(request.email, db)
    if not user or not bcrypt.checkpw(request.password.encode("utf-8"), user.password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {
        "message": f"Login successful! Redirect to {user.role.lower()} dashboard.",
        "role": user.role
    }
    
@router.post("/register")
async def register(request: RegisterRequest, db=Depends(get_db)):
    existing_user = await get_user_by_email(request.email, db)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = bcrypt.hashpw(request.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user_data = request.model_dump()
    user_data["password"] = hashed_pw
    user = await create_user(user_data)
    return {"message": "Registration successful!", "user_id": user.id, "role": user.role}
