from fastapi import APIRouter, Request, UploadFile, File, Query, HTTPException, Depends
from ..services.word_service import create_word, get_word_by_id, search_words, update_lang_entry, delete_word
from ..services.log_service import create_log
from ..models.word_model import WordModel
from ..utils import decode_token

router = APIRouter(prefix="/api", tags=["words"])

def get_user_from_request(request: Request):
    auth = request.headers.get("Authorization")
    if not auth:
        return None
    try:
        token = auth.split(" ")[1]
        payload = decode_token(token)
        return payload
    except Exception:
        return None

@router.post("/words/")
async def add_word(item: WordModel, request: Request):
    user = get_user_from_request(request)
    username = user.get("sub") if user else "anonymous"
    role = user.get("role") if user else "public"
    wid = await create_word(item)
    await create_log(username, role, "add", "translations", wid,
                     summary=f"新增词条 langs={list(item.lang_entries.keys())}", request=request)
    return {"id": wid}

@router.get("/words/{word_id}")
async def read_word(word_id: str):
    doc = await get_word_by_id(word_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Not found")
    return doc

@router.get("/words/search/")
async def search(q: str = Query(...), lang: str = "zh"):
    return await search_words(q, lang)

@router.put("/words/{word_id}/{lang_code}")
async def update_entry(word_id: str, lang_code: str, entry: dict, request: Request):
    user = get_user_from_request(request)
    username = user.get("sub") if user else "anonymous"
    role = user.get("role") if user else "public"
    before = await get_word_by_id(word_id)
    await update_lang_entry(word_id, lang_code, entry)
    after = await get_word_by_id(word_id)
    await create_log(username, role, "update", "translations", word_id,
                     summary=f"更新 {lang_code} 字段", request=request, diff={"before": before, "after": after})
    return {"status": "ok"}

@router.delete("/words/{word_id}")
async def remove_word(word_id: str, request: Request):
    user = get_user_from_request(request)
    username = user.get("sub") if user else "anonymous"
    role = user.get("role") if user else "public"
    doc = await get_word_by_id(word_id)
    await delete_word(word_id)
    await create_log(username, role, "delete", "translations", word_id,
                     summary=f"删除词条", request=request, note=str(doc))
    return {"status": "deleted"}

@router.post("/words/batch_import/")
async def batch_import(file: UploadFile = File(...), request: Request = None):
    content = await file.read()
    import json
    try:
        data_list = json.loads(content)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    inserted = []
    for item in data_list:
        try:
            item.setdefault("added_by", "batch")
            res = await create_word(WordModel(**item))
            inserted.append(res)
        except Exception:
            continue
    user = get_user_from_request(request)
    username = user.get("sub") if user else "anonymous"
    await create_log(username, user.get("role") if user else "public", "import", "translations", ",".join(inserted),
                     summary=f"批量导入 {len(inserted)} 条", request=request)
    return {"inserted": inserted}
