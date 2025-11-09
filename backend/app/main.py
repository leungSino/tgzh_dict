from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth_routes, word_routes, log_routes, lemma_routes
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="tgzh_dict Backend")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(auth_routes.router)
app.include_router(word_routes.router)
app.include_router(lemma_routes.router)
app.include_router(log_routes.router)

# Serve frontend build if exists (optional)
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist")
if os.path.isdir(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")
