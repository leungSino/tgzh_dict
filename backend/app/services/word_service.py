from ..db import words_col
from ..models.word_model import WordModel
from bson import ObjectId

async def create_word(word: WordModel):
    data = word.dict()
    res = await words_col.insert_one(data)
    return str(res.inserted_id)

async def get_word_by_id(word_id: str):
    doc = await words_col.find_one({"_id": ObjectId(word_id)})
    if not doc:
        return None
    doc["_id"] = str(doc["_id"])
    return doc

async def search_words(q: str, lang: str = "zh", limit: int = 50):
    cursor = words_col.find({f"lang_entries.{lang}.word": {"$regex": q, "$options": "i"}}).limit(limit)
    res = []
    async for d in cursor:
        d["_id"] = str(d["_id"])
        res.append(d)
    return res

async def update_lang_entry(word_id: str, lang: str, entry: dict):
    await words_col.update_one({"_id": ObjectId(word_id)}, {"$set": {f"lang_entries.{lang}": entry}})
    return True

async def delete_word(word_id: str):
    await words_col.delete_one({"_id": ObjectId(word_id)})
    return True
