# backend/app/db.py
from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGO_URI, DB_NAME

# MongoDB 客户端和数据库
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

# Collection 定义
users_col = db["users"]
translations_col = db["translations"]
lemmas_col = db["lemmas"]
logs_col = db["operation_logs"]

# -------------------------
# 依赖注入函数（FastAPI Depends 使用）
# -------------------------

def get_users_collection():
    return users_col

def get_translations_collection():
    return translations_col

def get_lemmas_collection():
    return lemmas_col

def get_logs_collection():
    return logs_col
