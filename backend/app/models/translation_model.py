# backend/app/models/translation_model.py
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


# === 子模型定义 ===
class DefinitionModel(BaseModel):
    source: Optional[str] = ''
    target: Optional[str] = ''


class ContextModel(BaseModel):
    source: Optional[str] = ''
    target: Optional[str] = ''


class TranslationItemModel(BaseModel):
    key: Optional[str] = None  # 前端生成的 UUID，不强制
    translation: str
    searchTexts: Optional[List[str]] = Field(default_factory=list)
    posArray: Optional[List[str]] = Field(default_factory=list)
    definition: Optional[DefinitionModel] = Field(default_factory=DefinitionModel)
    context: Optional[ContextModel] = Field(default_factory=ContextModel)


# === 主模型 ===
class TranslationModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    sourceLang: str
    targetLang: str
    sourceText: str
    lemma: Optional[str] = None
    lemma_id: Optional[PyObjectId] = None
    root: Optional[str] = None
    description: Optional[str] = None

    translations: Optional[List[TranslationItemModel]] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    status: str = Field(default="draft")  # draft / published / archived

    class Config:
        json_encoders = {ObjectId: str}
        from_attributes = True
