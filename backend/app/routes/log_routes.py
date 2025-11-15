from fastapi import APIRouter, Query, Depends, Request, HTTPException
from typing import Optional
from ..services import log_service
from ..models.log_model import LogListResponse
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

@router.get("/logs", response_model=LogListResponse)
async def list_logs(
    skip: int = 0,
    limit: int = 50,
    user: Optional[str] = Query(None),
    action: Optional[str] = Query(None),
    current=Depends(require_admin)
):
    return await log_service.get_logs(skip=skip, limit=limit, user=user, action=action)

@router.delete("/logs/{log_id}")
async def remove_log(log_id: str, current=Depends(require_admin)):
    deleted_count = await log_service.delete_log(log_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="日志不存在")
    return {"deleted": deleted_count}

@router.delete("/logs")
async def remove_all_logs(current=Depends(require_admin)):
    deleted_count = await log_service.clear_logs()
    return {"deleted": deleted_count}
