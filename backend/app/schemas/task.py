from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
from dateutil.parser import parse as dateutil_parse

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: bool = False

    @field_validator("due_date", mode="before")
    @classmethod
    def parse_due_date(cls, v):
        if isinstance(v, str):
            try:
                return dateutil_parse(v)
            except Exception:
                raise ValueError("Format de date invalide")
        return v

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int

    class Config:
        from_attributes = True  # Pour FastAPI >= 0.95 / Pydantic v2

class TaskOut(TaskRead):
    pass
