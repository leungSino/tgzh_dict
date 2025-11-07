from fastapi import APIRouter, Depends
from ..models.word_model import WordModel
from ..services.word_service import WordService
from ..db import get_words_collection

router = APIRouter(prefix="/words", tags=["Words"])


@router.post("/", response_model=WordModel)
async def create_word(word: WordModel, collection=Depends(get_words_collection)):
    service = WordService(collection)
    return await service.create_word(word.dict(by_alias=True, exclude_none=True))


@router.get("/{word_id}", response_model=WordModel)
async def get_word(word_id: str, collection=Depends(get_words_collection)):
    service = WordService(collection)
    return await service.get_word(word_id)


@router.get("/", response_model=list[WordModel])
async def get_all_words(collection=Depends(get_words_collection)):
    service = WordService(collection)
    return await service.get_all_words()


@router.put("/{word_id}", response_model=WordModel)
async def update_word(word_id: str, word: WordModel, collection=Depends(get_words_collection)):
    service = WordService(collection)
    return await service.update_word(word_id, word.dict(by_alias=True, exclude_none=True))


@router.delete("/{word_id}")
async def delete_word(word_id: str, collection=Depends(get_words_collection)):
    service = WordService(collection)
    return {"deleted": await service.delete_word(word_id)}
