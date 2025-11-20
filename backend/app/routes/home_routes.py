from fastapi import APIRouter
from typing import List
from ..models.home_model import TranslateRequest, TranslateResult
from ..services.home_service import home_translate_text

router = APIRouter()

@router.post("/home/translate")
async def home_translate(req: TranslateRequest) -> dict:
    results: List[TranslateResult] = await home_translate_text(
        req.sourceText, req.sourceLang, req.targetLang
    )
    return {
        "success": bool(results),
        "results": results
    }
