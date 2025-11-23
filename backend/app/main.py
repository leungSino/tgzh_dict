from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth_routes, user_routes, translation_routes, log_routes, lemma_routes, home_routes
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from .logger import logger
import os

app = FastAPI(title="tgzh_dict Backend")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # 前端地址
    allow_credentials=True,
    allow_methods=["*"],   # GET, POST, PUT, DELETE, OPTIONS
    allow_headers=["*"],   # Authorization, Content-Type 等
)

# 测试CORS的端点
@app.get("/test-cors")
async def test_cors():
    return JSONResponse({"message": "CORS test successful", "timestamp": "now"})

@app.get("/ping")
async def ping():
    logger.info("Ping 请求被调用")
    return {"msg": "pong"}

# 全局OPTIONS处理器
@app.options("/{path:path}")
async def options_handler(path: str):
    return JSONResponse(content={}, status_code=200)

app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(translation_routes.router)
app.include_router(lemma_routes.router)
app.include_router(log_routes.router)
app.include_router(home_routes.router)

# Serve frontend build if exists (optional)
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist")
if os.path.isdir(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")
