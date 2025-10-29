from decouple import config

# MongoDB 连接
MONGO_URI = config("MONGO_URI", default="mongodb://localhost:27017")
DB_NAME = config("DB_NAME", default="polyglot_db")  # 明确指定数据库名

# JWT 配置
JWT_SECRET = config("JWT_SECRET", default="cici163163")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(config("ACCESS_TOKEN_EXPIRE_MINUTES", default=60*24*7))
