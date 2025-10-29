from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[str] = "editor"

class UserInDB(BaseModel):
    username: str
    password_hash: str
    role: str = "editor"
    created_at: datetime = Field(default_factory=datetime.utcnow)
