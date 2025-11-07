# backend/app/routes/lemma_routes.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..models.lemma_model import LemmaModel
from ..services.lemma_service import LemmaService
from ..db import get_lemmas_collection

router = APIRouter(prefix="/lemmas", tags=["Lemmas"])


@router.post("/", response_model=LemmaModel)
async def create_lemma(lemma: LemmaModel, collection=Depends(get_lemmas_collection)):
    service = LemmaService(collection)
    return await service.create_lemma(lemma.dict(by_alias=True, exclude_none=True))


@router.get("/{lemma_id}", response_model=LemmaModel)
async def get_lemma(lemma_id: str, collection=Depends(get_lemmas_collection)):
    service = LemmaService(collection)
    lemma = await service.get_lemma(lemma_id)
    if not lemma:
        raise HTTPException(status_code=404, detail="Lemma not found")
    return lemma


@router.get("/", response_model=List[LemmaModel])
async def get_all_lemmas(collection=Depends(get_lemmas_collection)):
    service = LemmaService(collection)
    return await service.get_all_lemmas()


@router.put("/{lemma_id}", response_model=LemmaModel)
async def update_lemma(lemma_id: str, lemma: LemmaModel, collection=Depends(get_lemmas_collection)):
    service = LemmaService(collection)
    updated = await service.update_lemma(lemma_id, lemma.dict(by_alias=True, exclude_none=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Lemma not found or not modified")
    return updated


@router.delete("/{lemma_id}")
async def delete_lemma(lemma_id: str, collection=Depends(get_lemmas_collection)):
    service = LemmaService(collection)
    deleted = await service.delete_lemma(lemma_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Lemma not found")
    return {"deleted": deleted}
