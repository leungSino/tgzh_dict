from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

class LogBase(BaseModel):
    user: str
    role: str
    action: str
    target_collection: str
    target_id: str
    target_summary: str
    note: Optional[str] = ""
    diff: Optional[Dict] = {}

class LogCreate(LogBase):
    pass

class LogInDB(LogBase):
    id: str = Field(..., alias="_id")
    timestamp: datetime

class LogListResponse(BaseModel):
    items: list[LogInDB]
    total: int
