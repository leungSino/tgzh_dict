#!/usr/bin/env bash
# from backend/ directory
source .venv/bin/activate || source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
