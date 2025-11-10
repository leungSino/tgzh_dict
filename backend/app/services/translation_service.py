from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from datetime import datetime
from fastapi import Request
from ..services.log_service import create_log


class TranslationService:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def create_translation(self, data: dict, request: Request = None, user: str = None, role: str = None) -> dict:
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()
        result = await self.collection.insert_one(data)
        doc = await self.collection.find_one({"_id": result.inserted_id})

        await create_log(user=user, role=role, action="create", target_collection="translations",
                         target_id=result.inserted_id, summary=data.get("sourceText", ""), request=request)
        return doc

    async def get_translation(self, translation_id: str) -> Optional[dict]:
        return await self.collection.find_one({"_id": ObjectId(translation_id)})

    async def get_all_translations(self, limit: int = 100) -> List[dict]:
        cursor = self.collection.find().limit(limit)
        return await cursor.to_list(length=limit)

    async def update_translation(self, translation_id: str, data: dict,
                                 request: Request = None, user: str = None, role: str = None) -> Optional[dict]:
        old_doc = await self.get_translation(translation_id)
        if not old_doc:
            return None

        data["updated_at"] = datetime.utcnow()
        await self.collection.update_one({"_id": ObjectId(translation_id)}, {"$set": data})
        new_doc = await self.get_translation(translation_id)

        diff = {k: {"old": old_doc.get(k), "new": new_doc.get(k)} for k in data if old_doc.get(k) != new_doc.get(k)}
        await create_log(user=user, role=role, action="update", target_collection="translations",
                         target_id=translation_id, summary=new_doc.get("sourceText", ""), request=request, diff=diff)
        return new_doc

    async def delete_translation(self, translation_id: str, request: Request = None,
                                 user: str = None, role: str = None) -> bool:
        doc = await self.get_translation(translation_id)
        if not doc:
            return False
        result = await self.collection.delete_one({"_id": ObjectId(translation_id)})

        await create_log(user=user, role=role, action="delete", target_collection="translations",
                         target_id=translation_id, summary=doc.get("sourceText", ""), request=request)
        return result.deleted_count > 0
