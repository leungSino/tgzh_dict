from fastapi import APIRouter, HTTPException
from ..models.user_model import UserCreate
from ..services.auth_service import register_user, authenticate_user
from fastapi import APIRouter, Form


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(data: UserCreate):
    uid = await register_user(data)
    if not uid:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"user_id": uid}


@router.post("/login")
async def login(data: UserCreate):
    res = await authenticate_user(data.username, data.password)
    if not res:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": res["token"], "token_type": "bearer", "username": res["username"], "role": res["role"]}


