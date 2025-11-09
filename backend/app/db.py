# backend/app/db.py
from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGO_URI, DB_NAME

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

users_col = db["users"]
words_col = db["words"]
lemmas_col = db["lemmas"]
logs_col = db["operation_logs"]

# 依赖注入用函数返回 collection
def get_words_collection():
    return words_col

def get_lemmas_collection():
    return lemmas_col

def get_users_collection():
    return users_col

def get_logs_collection():
    return logs_col