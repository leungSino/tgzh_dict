from ..db import users_col
from ..utils import hash_password, verify_password, create_access_token
from ..models.user_model import UserCreate

async def register_user(user: UserCreate):
    existing = await users_col.find_one({"username": user.username})
    if existing:
        return None
    pw = hash_password(user.password)
    doc = {"username": user.username, "password_hash": pw, "role": user.role}
    res = await users_col.insert_one(doc)
    return str(res.inserted_id)

async def authenticate_user(username: str, password: str):
    user = await users_col.find_one({"username": username})
    if not user:
        return None
    if not verify_password(password, user["password_hash"]):
        return None
    token = create_access_token({"sub": username, "role": user.get("role", "editor")})
    # 返回 token 和用户信息
    return {"token": token, "username": user["username"], "role": user.get("role", "editor")}


async def get_user_by_username(username: str):
    return await users_col.find_one({"username": username})
