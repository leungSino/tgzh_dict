from fastapi import APIRouter, Query, Depends, Request, HTTPException, Body
from typing import Optional
from ..models.user_model import UserCreate
from ..services.user_service import register_user, get_users, update_user_by_username, get_user_by_username
from ..utils import decode_token
from ..db import users_col

router = APIRouter(prefix="/admin", tags=["admin"])

# -----------------------
# 权限校验
# -----------------------
def require_admin(request: Request):
    auth = request.headers.get("Authorization")
    if not auth:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = auth.split(" ")[1]
    payload = decode_token(token)
    if not payload or payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return payload

# -----------------------
# 查询用户列表
# -----------------------
@router.get("/users")
async def list_users(
    skip: int = 0,
    limit: int = 50,
    username: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    current=Depends(require_admin)
):
    query = {}
    if username:
        query["username"] = {"$regex": username, "$options": "i"}
    if role:
        query["role"] = role

    cursor = users_col.find(query).sort("created_at", -1).skip(skip).limit(limit)
    users = []
    async for u in cursor:
        u["_id"] = str(u["_id"])
        users.append(u)
    total = await users_col.count_documents(query)
    return {"data": users, "total": total}

# -----------------------
# 新增用户
# -----------------------
@router.post("/users")
async def create_user(user: UserCreate, current=Depends(require_admin)):
    inserted_id = await register_user(user)
    if not inserted_id:
        raise HTTPException(status_code=400, detail="用户名已存在")
    return {"_id": inserted_id}

# -----------------------
# 编辑用户
# -----------------------
@router.put("/users/{username}")
async def edit_user(username: str, update_data: dict = Body(...), current=Depends(require_admin)):
    existing = await get_user_by_username(username)
    if not existing:
        raise HTTPException(status_code=404, detail="用户不存在")
    modified_count = await update_user_by_username(username, update_data)
    return {"modified_count": modified_count}

# -----------------------
# 删除用户
# -----------------------
@router.delete("/users/{username}")
async def delete_user(username: str, current=Depends(require_admin)):
    existing = await get_user_by_username(username)
    if not existing:
        raise HTTPException(status_code=404, detail="用户不存在")
    res = await users_col.delete_one({"username": username})
    return {"deleted_count": res.deleted_count}
