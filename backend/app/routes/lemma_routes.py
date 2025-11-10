from fastapi import APIRouter, Query, Depends, Request, HTTPException
from typing import Optional
from ..models.lemma_model import LemmaModel
from ..services.lemma_service import LemmaService
from ..db import get_lemmas_collection
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


@router.post("/lemmas", response_model=LemmaModel)
async def create_lemma(lemma: LemmaModel, collection=Depends(get_lemmas_collection), current=Depends(require_admin)):
    service = LemmaService(collection)
    return await service.create_lemma(lemma.dict(by_alias=True, exclude_none=True))


@router.get("/lemmas", response_model=dict)
async def get_lemmas(
    skip: int = 0,
    limit: int = 50,
    lemma: Optional[str] = Query(None),
    collection=Depends(get_lemmas_collection),
    current=Depends(require_admin)
):
    service = LemmaService(collection)
    q = {}
    if lemma:
        q["lemma"] = {"$regex": lemma, "$options": "i"}
    total = await collection.count_documents(q)
    cursor = collection.find(q).skip(skip).limit(limit)
    data = []
    async for item in cursor:
        item["_id"] = str(item["_id"])
        data.append(item)
    return {"data": data, "total": total}


@router.get("/lemmas/{lemma_id}", response_model=LemmaModel)
async def get_lemma(lemma_id: str, collection=Depends(get_lemmas_collection), current=Depends(require_admin)):
    service = LemmaService(collection)
    lemma = await service.get_lemma(lemma_id)
    if not lemma:
        raise HTTPException(status_code=404, detail="Lemma not found")
    return lemma


@router.put("/lemmas/{lemma_id}", response_model=LemmaModel)
async def update_lemma(lemma_id: str, lemma: LemmaModel, collection=Depends(get_lemmas_collection), current=Depends(require_admin)):
    service = LemmaService(collection)
    updated = await service.update_lemma(lemma_id, lemma.dict(by_alias=True, exclude_none=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Lemma not found or not modified")
    return updated


@router.delete("/lemmas/{lemma_id}")
async def delete_lemma(lemma_id: str, collection=Depends(get_lemmas_collection), current=Depends(require_admin)):
    service = LemmaService(collection)
    deleted = await service.delete_lemma(lemma_id)
    return {"deleted": deleted}
