from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

class LangEntry(BaseModel):
    word: str
    definition: Optional[str] = None
    examples: Optional[List[dict]] = []

class WordModel(BaseModel):
    lang_entries: Dict[str, LangEntry]
    relations: Optional[Dict[str, bool]] = {}
    tags: Optional[List[str]] = []
    added_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
