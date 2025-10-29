from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException, Request
from .config import JWT_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# 使用 pbkdf2_sha256，避免 bcrypt 72 字节限制
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    password = str(password).strip()  # 确保是字符串并去掉前后空格
    if len(password.encode("utf-8")) > 1024:  # 防止超长攻击
        raise ValueError("密码过长")
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    plain = str(plain).strip()
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: int = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=(expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def decode_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_client_ip(request: Request) -> str:
    try:
        return request.client.host if request and request.client else ""
    except Exception:
        return ""
