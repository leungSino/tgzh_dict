from ..db import users_col
from ..utils import hash_password, verify_password, create_access_token
from ..models.user_model import UserCreate
from ..services.log_service import create_log
from datetime import datetime
from fastapi import Request
from typing import Optional


# 注册用户
async def register_user(user: UserCreate, request: Request = None, operator: str = None, role: str = None):
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
        "created_by": getattr(user, "created_by", operator or "system"),
        "updated_by": getattr(user, "created_by", operator or "system"),
    }
    res = await users_col.insert_one(doc)
    new_id = str(res.inserted_id)

    await create_log(
        user=operator,
        role=role,
        action="create",
        target_collection="users",
        target_id=new_id,
        summary=f"创建用户：{user.username}",
        request=request,
    )
    return new_id


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

# 检查用户名是否存在
async def check_username_exists(username: str):
    """检查用户名是否存在"""
    user = await users_col.find_one({"username": username}, {"_id": 1})
    return user is not None, str(user["_id"]) if user else None

# 更新用户
async def update_user_by_username(username: str, update_data: dict, request: Request = None, operator: str = None, role: str = None):
    old_doc = await users_col.find_one({"username": username})
    if not old_doc:
        return 0

    update_doc = update_data.copy()
    if "password" in update_doc:
        update_doc["password_hash"] = hash_password(update_doc.pop("password"))
    update_doc["updated_at"] = datetime.utcnow()
    update_doc["updated_by"] = operator or "system"

    await users_col.update_one({"username": username}, {"$set": update_doc})
    new_doc = await users_col.find_one({"username": username})

    diff = {k: {"old": old_doc.get(k), "new": new_doc.get(k)} for k in update_doc if old_doc.get(k) != new_doc.get(k)}

    await create_log(
        user=operator,
        role=role,
        action="update",
        target_collection="users",
        target_id=str(old_doc["_id"]),
        summary=f"更新用户：{username}",
        request=request,
        diff=diff,
    )
    return 1


# 删除用户
async def delete_user_by_username(username: str, request: Request = None, operator: str = None, role: str = None):
    doc = await users_col.find_one({"username": username})
    if not doc:
        return False

    res = await users_col.delete_one({"username": username})
    await create_log(
        user=operator,
        role=role,
        action="delete",
        target_collection="users",
        target_id=str(doc["_id"]),
        summary=f"删除用户：{username}",
        request=request,
    )
    return res.deleted_count > 0
