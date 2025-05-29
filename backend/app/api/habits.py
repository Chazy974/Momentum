from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.habit import Habit
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter(prefix="/habits", tags=["habits"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class HabitBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True

class HabitCreate(HabitBase):
    pass

class HabitUpdate(HabitBase):
    pass

class HabitOut(HabitBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

@router.get("/", response_model=List[HabitOut])
def get_habits(db: Session = Depends(get_db)):
    return db.query(Habit).all()

@router.post("/", response_model=HabitOut)
def create_habit(habit: HabitCreate, db: Session = Depends(get_db)):
    db_habit = Habit(**habit.dict())
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

@router.put("/{habit_id}", response_model=HabitOut)
def update_habit(habit_id: int, habit: HabitUpdate, db: Session = Depends(get_db)):
    db_habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    for key, value in habit.dict(exclude_unset=True).items():
        setattr(db_habit, key, value)
    db.commit()
    db.refresh(db_habit)
    return db_habit

@router.delete("/{habit_id}")
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    db_habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    db.delete(db_habit)
    db.commit()
    return {"detail": "Habit deleted"}
