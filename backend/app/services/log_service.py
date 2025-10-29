from ..db import logs_col
from datetime import datetime
from fastapi import Request

async def create_log(user: str, role: str, action: str, target_collection: str,
                     target_id: str, summary: str, request: Request = None, note: str = "", diff: dict = None):
    try:
        ip = request.client.host if request and request.client else ""
    except Exception:
        ip = ""
    doc = {
        "user": user or "anonymous",
        "role": role or "public",
        "action": action,
        "target_collection": target_collection,
        "target_id": str(target_id),
        "target_summary": summary,
        "timestamp": datetime.utcnow().isoformat(),
        "ip_address": ip,
        "note": note,
        "diff": diff or {}
    }
    await logs_col.insert_one(doc)
