from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime
from ..services.log_service import create_log
from fastapi import Request


class LemmaService:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def create_lemma(
        self,
        data: dict,
        request: Request = None,
        operator: str = None,
        role: str = None
    ) -> dict:
        # 补充时间字段
        data.setdefault("created_at", datetime.utcnow())
        data.setdefault("updated_at", datetime.utcnow())
        data.pop("_id", None)  # MongoDB 自动生成 _id

        result = await self.collection.insert_one(data)
        doc = await self.collection.find_one({"_id": result.inserted_id})
        doc["_id"] = str(doc["_id"])

        await create_log(
            user=operator,
            role=role,
            action="create",
            target_collection="lemmas",
            target_id=str(result.inserted_id),
            summary=data.get("lemma", ""),
            request=request
        )
        return doc

    async def search_lemmas(self, query: str, limit: int = 10) -> List[dict]:
        cursor = self.collection.find(
            {"lemma": {"$regex": query, "$options": "i"}},
            {"_id": 1, "lemma": 1}
        ).limit(limit)

        results = []
        async for doc in cursor:
            results.append({"_id": str(doc["_id"]), "lemma": doc["lemma"]})
        return results

    async def check_lemma_exists(self, lemma: str) -> dict:
        doc = await self.collection.find_one({"lemma": lemma})
        if doc:
            return {"exists": True, "lemma_id": str(doc["_id"])}
        return {"exists": False}

    async def get_lemma(self, lemma_id: str) -> Optional[dict]:
        try:
            oid = ObjectId(lemma_id)
        except InvalidId:
            return None

        doc = await self.collection.find_one({"_id": oid})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def get_all_lemmas(self, skip: int = 0, limit: int = 100, query: dict = None) -> dict:
        query = query or {}
        total = await self.collection.count_documents(query)
        cursor = self.collection.find(query).skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)
        for doc in docs:
            doc["_id"] = str(doc["_id"])
        return {"data": docs, "total": total}

    async def update_lemma(
        self,
        lemma_id: str,
        data: dict,
        request: Request = None,
        operator: str = None,
        role: str = None
    ) -> Optional[dict]:
        old_doc = await self.get_lemma(lemma_id)
        if not old_doc:
            return None

        data["updated_at"] = datetime.utcnow()
        await self.collection.update_one({"_id": ObjectId(lemma_id)}, {"$set": data})
        new_doc = await self.get_lemma(lemma_id)

        diff = {k: {"old": old_doc.get(k), "new": new_doc.get(k)} for k in data if old_doc.get(k) != new_doc.get(k)}

        await create_log(
            user=operator,
            role=role,
            action="update",
            target_collection="lemmas",
            target_id=lemma_id,
            summary=new_doc.get("lemma", ""),
            request=request,
            diff=diff
        )
        return new_doc

    async def delete_lemma(
        self,
        lemma_id: str,
        request: Request = None,
        operator: str = None,
        role: str = None
    ) -> bool:
        doc = await self.get_lemma(lemma_id)
        if not doc:
            return False

        result = await self.collection.delete_one({"_id": ObjectId(lemma_id)})

        await create_log(
            user=operator,
            role=role,
            action="delete",
            target_collection="lemmas",
            target_id=lemma_id,
            summary=doc.get("lemma", ""),
            request=request
        )
        return result.deleted_count > 0
