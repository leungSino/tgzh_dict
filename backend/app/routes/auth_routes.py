from fastapi import APIRouter, HTTPException
from ..models.user_model import UserCreate
from ..services.user_service import register_user, authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(data: UserCreate):
    res = await authenticate_user(data.username, data.password)
    if not res:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if res.get("disabled"):
        raise HTTPException(status_code=403, detail="Account disabled")
    return {
        "access_token": res["token"],
        "token_type": "bearer",
        "username": res["username"],
        "role": res["role"],
        "status": res["status"],
    }
