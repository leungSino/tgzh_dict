from ..db import users_col
from ..utils import hash_password, verify_password, create_access_token
from ..models.user_model import UserCreate
from datetime import datetime
from typing import Optional


# 注册用户
async def register_user(user: UserCreate):
    existing = await users_col.find_one({"username": user.username})
    if existing:
        return None

    pw = hash_password(user.password)
    doc = {
        "username": user.username,
        "password_hash": pw,
        "role": user.role,
        "status": user.status or "enabled",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "created_by": getattr(user, "created_by", "system"),
        "updated_by": getattr(user, "created_by", "system"),
    }
    res = await users_col.insert_one(doc)
    return str(res.inserted_id)


# 用户登录
async def authenticate_user(username: str, password: str):
    user = await users_col.find_one({"username": username})
    if not user:
        return None
    if not verify_password(password, user["password_hash"]):
        return None
    if user.get("status") == "disabled":
        return {"disabled": True}

    token = create_access_token({"sub": username, "role": user.get("role", "editor")})
    return {
        "token": token,
        "username": user["username"],
        "role": user.get("role", "editor"),
        "status": user.get("status", "enabled"),
    }


# 获取单个用户
async def get_user_by_username(username: str):
    return await users_col.find_one({"username": username})


# 获取用户列表
async def get_users(skip: int = 0, limit: int = 1000):
    cursor = users_col.find().skip(skip).limit(limit)
    return await cursor.to_list(length=limit)


# 更新用户
async def update_user_by_username(username: str, update_data: dict):
    update_doc = update_data.copy()
    if "password" in update_doc:
        update_doc["password_hash"] = hash_password(update_doc.pop("password"))
    update_doc["updated_at"] = datetime.utcnow()
    res = await users_col.update_one({"username": username}, {"$set": update_doc})
    return res.modified_count
