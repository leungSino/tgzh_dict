from ..db import logs_col
from datetime import datetime
from fastapi import Request
from typing import Optional, Dict
from bson import ObjectId

async def create_log(
    user: str,
    role: str,
    action: str,
    target_collection: str,
    target_id: str,
    summary: str,
    request: Optional[Request] = None,
    note: str = "",
    diff: Optional[Dict] = None
):
    """创建日志记录"""
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
        "timestamp": datetime.utcnow(),
        "ip_address": ip,
        "note": note,
        "diff": diff or {}
    }
    await logs_col.insert_one(doc)
    doc["_id"] = str(doc["_id"]) if "_id" in doc else None
    return doc

async def get_logs(
    skip: int = 0,
    limit: int = 50,
    user: Optional[str] = None,
    action: Optional[str] = None
):
    """查询日志列表"""
    query = {}
    if user:
        query["user"] = {"$regex": user, "$options": "i"}
    if action:
        query["action"] = {"$regex": action, "$options": "i"}

    cursor = logs_col.find(query).sort("timestamp", -1).skip(skip).limit(limit)
    items = []
    async for log in cursor:
        log["_id"] = str(log["_id"])
        items.append(log)

    total = await logs_col.count_documents(query)
    return {"items": items, "total": total}

async def delete_log(log_id: str):
    """删除单条日志"""
    try:
        oid = ObjectId(log_id)
    except Exception:
        return 0

    res = await logs_col.delete_one({"_id": oid})
    return res.deleted_count

async def clear_logs():
    """清空日志"""
    res = await logs_col.delete_many({})
    return res.deleted_count
