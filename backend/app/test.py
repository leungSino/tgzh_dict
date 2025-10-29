from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

print(hash_password("cici"))
