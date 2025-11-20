from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
from bson import ObjectId


class ExampleModel(BaseModel):
    tg: Optional[str] = ""
    zh: Optional[str] = ""
    ru: Optional[str] = ""
    en: Optional[str] = ""
    pos: Optional[List[str]] = []
    key: Optional[str] = None   # 前端唯一标识（不是 DB _id）


class LemmaModel(BaseModel):

    language: str
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
