# backend/app/services/lemma_service.py
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from datetime import datetime


class LemmaService:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def create_lemma(self, data: dict) -> dict:
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()
        result = await self.collection.insert_one(data)
        return await self.collection.find_one({"_id": result.inserted_id})

    async def get_lemma(self, lemma_id: str) -> Optional[dict]:
        return await self.collection.find_one({"_id": ObjectId(lemma_id)})

    async def get_all_lemmas(self, limit: int = 100) -> List[dict]:
        cursor = self.collection.find().limit(limit)
        return await cursor.to_list(length=limit)

    async def update_lemma(self, lemma_id: str, data: dict) -> Optional[dict]:
        data["updated_at"] = datetime.utcnow()
        await self.collection.update_one({"_id": ObjectId(lemma_id)}, {"$set": data})
        return await self.get_lemma(lemma_id)

    async def delete_lemma(self, lemma_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(lemma_id)})
        return result.deleted_count > 0
