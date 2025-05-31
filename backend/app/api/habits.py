from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.habit import Habit
from app.schemas.habit import HabitCreate, HabitUpdate, HabitRead
from typing import List

router = APIRouter(prefix="/habits", tags=["habits"])

# Dépendance DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Lire toutes les habitudes
@router.get("/", response_model=List[HabitRead])
def read_habits(db: Session = Depends(get_db)):
    try:
        habits = db.query(Habit).order_by(Habit.created_at.desc()).all()
        print(f"✅ {len(habits)} habitude(s) récupérées")
        return habits
    except Exception as e:
        print(f"❌ ERREUR read_habits: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des habitudes")

# Créer une habitude
@router.post("/", response_model=HabitRead)
def create_habit(habit: HabitCreate, db: Session = Depends(get_db)):
    try:
        db_habit = Habit(**habit.dict(), user_id=None)  # à adapter plus tard avec l’auth
        db.add(db_habit)
        db.commit()
        db.refresh(db_habit)
        return db_habit
    except Exception as e:
        print("❌ Erreur create_habit:", e)
        raise HTTPException(status_code=500, detail="Erreur lors de la création")

# Modifier une habitude
@router.put("/{habit_id}", response_model=HabitRead)
def update_habit(habit_id: int, habit: HabitUpdate, db: Session = Depends(get_db)):
    db_habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habitude introuvable")
    for key, value in habit.dict(exclude_unset=True).items():
        setattr(db_habit, key, value)
    db.commit()
    db.refresh(db_habit)
    return db_habit

# Supprimer une habitude
@router.delete("/{habit_id}")
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    db_habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habitude introuvable")
    db.delete(db_habit)
    db.commit()
    return {"detail": "Habitude supprimée"}
