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


class ExampleModel(BaseModel):
    source: str
    target: str
    pos: Optional[List[str]] = []
    key: Optional[str] = None  # 前端用于唯一标识（非数据库必需）


class LemmaModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    lemma: str
    root: Optional[str] = None
    isRoot: bool = False
    pos: Optional[List[str]] = None

    # 多语言释义
    definitions: Optional[Dict[str, str]] = Field(
        default_factory=lambda: {"tg": "", "zh": "", "ru": "", "en": ""}
    )

    # 动词变位
    conjugations: Optional[Dict[str, List[str]]] = Field(
        default_factory=lambda: {"past": [], "present": [], "future": []}
    )

    # 示例句子
    examples: Optional[List[ExampleModel]] = Field(default_factory=list)

    # 派生词、关联词
    derived: Optional[List[str]] = None
    related: Optional[List[str]] = None

    status: str = Field(default="draft")  # draft / published / archived

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None
    updated_by: Optional[str] = None

    class Config:
        json_encoders = {ObjectId: str}
        from_attributes = True
