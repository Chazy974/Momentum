from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from dateutil.parser import parse as dateutil_parse

class HabitLogBase(BaseModel):
    date: datetime
    value: Optional[str] = None

    @field_validator("date", mode="before")
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str):
            try:
                return dateutil_parse(v)
            except Exception:
                raise ValueError("Format de date invalide")
        return v

class HabitLogCreate(HabitLogBase):
    habit_id: int

class HabitLogUpdate(HabitLogBase):
    pass

class HabitLogRead(BaseModel):
    id: int
    habit_id: int
    date: datetime
    value: Optional[str] = None

    class Config:
        from_attributes = True
