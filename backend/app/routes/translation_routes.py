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
    if not payload or payload.get("role") not in ["admin", "editor"]:
        raise HTTPException(status_code=403, detail="Admin or Editor only")
    return payload


@router.post("/translations", response_model=TranslationModel)
async def create_translation(
        translation: TranslationModel,
        request: Request,
        collection=Depends(get_translations_collection),
        current=Depends(require_admin)
):
    service = TranslationService(collection)
    try:
        data_dict = translation.dict(exclude_none=True)
        data_dict.pop("_id", None)  # MongoDB 自动生成 _id
        result = await service.create_translation(
            data_dict,
            request=request,
            operator=current["sub"],  # 当前操作人
            role=current["role"]  # 当前操作人角色
        )
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")

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
            item["targetText"] = "; ".join([t.get("translation", "") for t in item["translations"]])

        data.append(item)
    return {"data": data, "total": total}

@router.get("/checksourcetext")
async def check_lemma(
    source_text: str = Query(..., min_length=1, description="要检查的源单词"),
    collection=Depends(get_translations_collection),
    current=Depends(require_admin)
):
    service = TranslationService(collection)
    return await service.check_source_text(source_text)

@router.get("/translations/{translation_id}", response_model=TranslationModel)
async def get_translation(translation_id: str, collection=Depends(get_translations_collection), current=Depends(require_admin)):
    service = TranslationService(collection)
    translation = await service.get_translation(translation_id)
    if not translation:
        raise HTTPException(status_code=404, detail="Translation not found")
    return translation


@router.put("/translations/{translation_id}", response_model=TranslationModel)
async def update_translation(
        translation_id: str,
        translation: TranslationModel,
        request: Request = None,
        collection=Depends(get_translations_collection),
        current=Depends(require_admin)
):
    service = TranslationService(collection)
    updated = await service.update_translation(
        translation_id,
        translation.dict(exclude_none=True),
        request = request,
        operator = current["sub"],  # 当前操作人
        role = current["role"]      # 当前操作人角色
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Translation not found or not modified")
    return updated


@router.delete("/translations/{translation_id}")
async def delete_translation(
        translation_id: str,
        request: Request = None,
        collection=Depends(get_translations_collection),
        current=Depends(require_admin)
):
    service = TranslationService(collection)
    deleted = await service.delete_translation(
        translation_id,
        request = request,
        operator = current["sub"],  # 当前操作人
        role = current["role"]      # 当前操作人角色
    )
    return {"deleted": deleted}
