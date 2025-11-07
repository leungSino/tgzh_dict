from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from datetime import datetime


class WordService:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def create_word(self, data: dict) -> dict:
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()
        result = await self.collection.insert_one(data)
        return await self.collection.find_one({"_id": result.inserted_id})

    async def get_word(self, word_id: str) -> Optional[dict]:
        return await self.collection.find_one({"_id": ObjectId(word_id)})

    async def get_all_words(self, limit: int = 100) -> List[dict]:
        cursor = self.collection.find().limit(limit)
        return await cursor.to_list(length=limit)

    async def update_word(self, word_id: str, data: dict) -> Optional[dict]:
        data["updated_at"] = datetime.utcnow()
        await self.collection.update_one(
            {"_id": ObjectId(word_id)}, {"$set": data}
        )
        return await self.get_word(word_id)

    async def delete_word(self, word_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(word_id)})
        return result.deleted_count > 0
