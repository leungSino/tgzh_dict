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
    if not payload or payload.get("role") not in ["admin", "editor"]:
        raise HTTPException(status_code=403, detail="Admin or Editor only")
    return payload


@router.post("/lemmas", response_model=LemmaModel)
async def create_lemma(
    lemma: LemmaModel,
    request: Request,
    collection=Depends(get_lemmas_collection),
    current=Depends(require_admin)
):
    service = LemmaService(collection)
    try:
        data_dict = lemma.dict(exclude_none=True)
        data_dict.pop("_id", None)  # MongoDB 自动生成 _id
        result = await service.create_lemma(
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


@router.get("/lemmas")
async def get_lemmas(
    skip: int = 0,
    limit: int = 50,
    lemma: Optional[str] = Query(None),
    collection=Depends(get_lemmas_collection),
    current=Depends(require_admin)
):
    service = LemmaService(collection)
    query = {}
    if lemma:
        query["lemma"] = {"$regex": lemma, "$options": "i"}
    result = await service.get_all_lemmas(skip=skip, limit=limit, query=query)
    return result


@router.get("/searchlemmas")
async def search_lemmas(
    q: Optional[str] = Query(None, description="搜索原型词"),
    limit: int = Query(10, description="返回条数"),
    collection=Depends(get_lemmas_collection),
    current=Depends(require_admin)
):
    if not q or not q.strip():
        return {"data": []}

    service = LemmaService(collection)
    results = await service.search_lemmas(q, limit)
    return {"data": results}


@router.get("/checklemma")
async def check_lemma(
    lemma: str = Query(..., min_length=1, description="要检查的原型词"),
    collection=Depends(get_lemmas_collection),
    current=Depends(require_admin)
):
    service = LemmaService(collection)
    return await service.check_lemma_exists(lemma)


@router.get("/lemmas/{lemma_id}", response_model=LemmaModel)
async def get_lemma(
    lemma_id: str,
    collection=Depends(get_lemmas_collection),
    current=Depends(require_admin)
):
    service = LemmaService(collection)
    lemma = await service.get_lemma(lemma_id)
    if not lemma:
        raise HTTPException(status_code=404, detail="Lemma not found")
    return lemma


@router.put("/lemmas/{lemma_id}", response_model=LemmaModel)
async def update_lemma(
    lemma_id: str,
    lemma: LemmaModel,
    request: Request = None,
    collection=Depends(get_lemmas_collection),
    current=Depends(require_admin)
):
    service = LemmaService(collection)
    updated = await service.update_lemma(
        lemma_id,
        lemma.dict(exclude_none=True),
        request = request,
        operator = current["sub"],  # 当前操作人
        role = current["role"]  # 当前操作人角色
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Lemma not found or not modified")
    return updated


@router.delete("/lemmas/{lemma_id}")
async def delete_lemma(
    lemma_id: str,
    request: Request = None,
    collection=Depends(get_lemmas_collection),
    current=Depends(require_admin)
):
    service = LemmaService(collection)
    deleted = await service.delete_lemma(
        lemma_id,
        request=request,
        operator=current["sub"],  # 当前操作人
        role=current["role"]  # 当前操作人角色
    )
    return {"deleted": deleted}
