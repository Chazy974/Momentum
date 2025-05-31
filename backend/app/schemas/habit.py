from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from dateutil.parser import parse as dateutil_parse
from enum import Enum

# Enum pour le type de cible
class HabitTargetType(str, Enum):
    boolean = "boolean"
    numeric = "numeric"
    time = "time"

class HabitBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True
    target_type: Optional[HabitTargetType] = None
    due_date: Optional[datetime] = None

    @field_validator("due_date", mode="before")
    @classmethod
    def parse_due_date(cls, v):
        if isinstance(v, str):
            try:
                return dateutil_parse(v)
            except Exception:
                raise ValueError("Format de date invalide")
        return v

class HabitCreate(HabitBase):
    pass

class HabitUpdate(HabitBase):
    pass

class HabitRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
