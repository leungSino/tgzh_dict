from fastapi import APIRouter, Query, Depends, Request, HTTPException
from typing import Optional
from ..models.translation_model import TranslationModel
from ..services.translation_service import TranslationService
from ..db import get_translations_collection
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


@router.post("/translations", response_model=TranslationModel)
async def create_translation(translation: TranslationModel, collection=Depends(get_translations_collection), current=Depends(require_admin)):
    service = TranslationService(collection)
    return await service.create_translation(translation.dict(by_alias=True, exclude_none=True))


@router.get("/translations", response_model=dict)
async def get_translations(
    skip: int = 0,
    limit: int = 50,
    query: Optional[str] = Query(None),
    collection=Depends(get_translations_collection),
    current=Depends(require_admin)
):
    service = TranslationService(collection)
    q = {}
    if query:
        q["$or"] = [
            {"sourceText": {"$regex": query, "$options": "i"}},
            {"targetText": {"$regex": query, "$options": "i"}},
            {"lemma": {"$regex": query, "$options": "i"}}
        ]

    total = await collection.count_documents(q)
    cursor = collection.find(q).skip(skip).limit(limit)
    data = []
    async for item in cursor:
        item["_id"] = str(item["_id"])
        if "translations" in item:
            item["targetText"] = "; ".join([t.get("translation", "") for t in item["translations"].values()])
        data.append(item)
    return {"data": data, "total": total}


@router.get("/translations/{translation_id}", response_model=TranslationModel)
async def get_translation(translation_id: str, collection=Depends(get_translations_collection), current=Depends(require_admin)):
    service = TranslationService(collection)
    translation = await service.get_translation(translation_id)
    if not translation:
        raise HTTPException(status_code=404, detail="Translation not found")
    return translation


@router.put("/translations/{translation_id}", response_model=TranslationModel)
async def update_translation(translation_id: str, translation: TranslationModel, collection=Depends(get_translations_collection), current=Depends(require_admin)):
    service = TranslationService(collection)
    updated = await service.update_translation(translation_id, translation.dict(by_alias=True, exclude_none=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Translation not found or not modified")
    return updated


@router.delete("/translations/{translation_id}")
async def delete_translation(translation_id: str, collection=Depends(get_translations_collection), current=Depends(require_admin)):
    service = TranslationService(collection)
    deleted = await service.delete_translation(translation_id)
    return {"deleted": deleted}
