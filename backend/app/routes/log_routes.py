from fastapi import APIRouter, Query, Depends, Request, HTTPException
from ..db import logs_col
from ..utils import decode_token
from typing import Optional

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

@router.get("/logs")
async def list_logs(skip: int = 0, limit: int = 50, action: Optional[str] = Query(None),
                    user: Optional[str] = Query(None), current=Depends(require_admin)):
    q = {}
    if action:
        q["action"] = action
    if user:
        q["user"] = user
    cursor = logs_col.find(q).sort("timestamp", -1).skip(skip).limit(limit)
    res = []
    async for d in cursor:
        d["_id"] = str(d["_id"])
        res.append(d)
    return res

@router.get("/logs/stats")
async def logs_stats(current=Depends(require_admin)):
    pipeline = [
        {"$group": {"_id": "$action", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    stats = await logs_col.aggregate(pipeline).to_list(length=50)
    return stats
