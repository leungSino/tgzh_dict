# backend/app/models/lemma_model.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


class LemmaModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    lemma: str
    root: Optional[str] = None
    isRoot: bool = False
    pos: Optional[List[str]] = None
    definition: Optional[Dict[str, str]] = None
    conjugations: Optional[Dict[str, List[str]]] = None
    examples: Optional[List[Dict[str, str]]] = None
    derived: Optional[List[str]] = None
    related: Optional[List[str]] = None
    notes: Optional[str] = None
    source: Optional[str] = None
    status: str = Field(default="draft")  # draft / published / archived

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None
    updated_by: Optional[str] = None

    class Config:
        json_encoders = {ObjectId: str}
        from_attributes = True
