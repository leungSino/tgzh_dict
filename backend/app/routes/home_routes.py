from fastapi import APIRouter, Query
from typing import List
from ..models.home_model import TranslateRequest, TranslateResult
from ..services.home_service import home_translate_text, get_lemma_by_lemma_service

router = APIRouter()

@router.post("/api/translate")
async def home_translate(req: TranslateRequest) -> dict:
    results: List[TranslateResult] = await home_translate_text(
        req.sourceText, req.sourceLang, req.targetLang
    )
    return {
        "success": bool(results),
        "results": results
    }

@router.get("/api/getlemma")
async def get_lemma_by_lemma(lemma: str = Query(..., min_length=1)):
    result = await get_lemma_by_lemma_service(lemma)

    if result:
        result = convert_mongo_id(result)

    return {
        "success": bool(result),
        "data": result
    }


def convert_mongo_id(doc: dict):
    """ 把 MongoDB 返回的 dict 中的 ObjectId 转成 str """
    if not doc:
        return doc
    doc["_id"] = str(doc["_id"])
    return doc
