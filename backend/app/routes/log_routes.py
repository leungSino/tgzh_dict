from fastapi import APIRouter, Query, Depends, Request, HTTPException
from typing import Optional
from ..db import logs_col
from ..utils import decode_token

router = APIRouter(prefix="/admin", tags=["admin"])


def require_admin(request: Request):
    auth = request.headers.get("Authorization")
    if not auth:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = auth.split(" ")[1]
    payload = decode_token(token)
    if not payload or payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return payload


# -----------------------
# 查询日志
# -----------------------
@router.get("/logs")
async def get_logs(
        skip: int = 0,
        limit: int = 50,
        user: Optional[str] = Query(None),
        action: Optional[str] = Query(None),
        current=Depends(require_admin)
):
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


# -----------------------
# 删除单条日志
# -----------------------
@router.delete("/logs/{log_id}")
async def delete_log(log_id: str, current=Depends(require_admin)):
    res = await logs_col.delete_one({"_id": log_id})
    return {"deleted": res.deleted_count}


# -----------------------
# 清空日志
# -----------------------
@router.delete("/logs")
async def clear_logs(current=Depends(require_admin)):
    res = await logs_col.delete_many({})
    return {"deleted": res.deleted_count}
