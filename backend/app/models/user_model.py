from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[str] = "editor"
    status: Optional[str] = "enabled"
    created_by: Optional[str] = None


class UserInDB(BaseModel):
    username: str
    password_hash: str
    role: str = "editor"
    status: str = "enabled"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
