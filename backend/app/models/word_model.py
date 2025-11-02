from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime


class ExampleItem(BaseModel):
    sentence: str
    translation: Optional[str] = None


class LangEntry(BaseModel):
    word: str = Field(..., description="该语言中的单词或短语")
    definition: Optional[str] = Field(None, description="释义或解释")
    examples: List[ExampleItem] = Field(default_factory=list, description="例句列表")


class WordModel(BaseModel):
    """多语言词条模型"""
    id: Optional[str] = Field(None, alias="_id", description="MongoDB文档ID")
    lang_entries: Dict[str, LangEntry] = Field(..., description="不同语言的词条信息，如 zh、tg、en、ru")
    relations: Dict[str, bool] = Field(default_factory=dict, description="单词之间的关系标识（如同义、反义）")
    tags: List[str] = Field(default_factory=list, description="标签，如 'verb', 'common', 'academic'")
    added_by: Optional[str] = Field(None, description="添加该词的用户ID或用户名")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
        validate_by_name = True  # Pydantic v2 替代 allow_population_by_field_name
        json_schema_extra = {
            "example": {
                "lang_entries": {
                    "zh": {
                        "word": "学习",
                        "definition": "掌握知识",
                        "examples": [{"sentence": "我喜欢学习。", "translation": "I like studying."}]
                    },
                    "tg": {
                        "word": "омӯхтан",
                        "definition": "ба даст овардани дониш",
                        "examples": [{"sentence": "Ман ҳар рӯз меомӯзам.", "translation": "我每天学习。"}]
                    },
                    "en": {
                        "word": "study",
                        "definition": "to learn",
                        "examples": [{"sentence": "I study every day.", "translation": "我每天学习。"}]
                    },
                    "ru": {
                        "word": "учиться",
                        "definition": "приобретать знания",
                        "examples": [{"sentence": "Я учусь каждый день.", "translation": "我每天学习。"}]
                    }
                },
                "relations": {"synonym": False, "antonym": False},
                "tags": ["verb", "common"],
                "added_by": "admin",
                "created_at": "2025-11-02T10:00:00Z"
            }
        }
