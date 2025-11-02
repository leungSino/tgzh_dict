from ..db import words_col
from ..models.word_model import WordModel
from bson import ObjectId


def _format_doc(doc: dict) -> dict:
    """把 MongoDB 的 _id 转成 id，并保持其他字段不变"""
    if not doc:
        return None
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc


# 创建词条
async def create_word(word: WordModel):
    data = word.dict(by_alias=True)
    res = await words_col.insert_one(data)
    return str(res.inserted_id)


# 获取全部词条
async def list_words(limit: int = 200):
    cursor = words_col.find().sort("created_at", -1).limit(limit)
    res = []
    async for d in cursor:
        res.append(_format_doc(d))
    return res


# 根据 ID 获取词条
async def get_word_by_id(word_id: str):
    doc = await words_col.find_one({"_id": ObjectId(word_id)})
    return _format_doc(doc)


# 搜索词条
async def search_words(q: str, lang: str = "zh", limit: int = 50):
    cursor = words_col.find({f"lang_entries.{lang}.word": {"$regex": q, "$options": "i"}}).limit(limit)
    res = []
    async for d in cursor:
        res.append(_format_doc(d))
    return res


# 更新语言字段
async def update_lang_entry(word_id: str, lang: str, entry: dict):
    await words_col.update_one({"_id": ObjectId(word_id)}, {"$set": {f"lang_entries.{lang}": entry}})
    return True

# 更新整个语言字段
async def update_word_full(word_id: str, item: WordModel):
    await words_col.update_one(
        {"_id": ObjectId(word_id)},
        {"$set": item.dict()}
    )

# 删除词条
async def delete_word(word_id: str):
    await words_col.delete_one({"_id": ObjectId(word_id)})
    return True
