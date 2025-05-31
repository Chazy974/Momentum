from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.habit_log import HabitLog
from app.schemas.habit_log import HabitLogCreate, HabitLogUpdate, HabitLogRead
from typing import List

router = APIRouter(prefix="/habit-logs", tags=["habit_logs"])

# Dépendance DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Lire tous les logs
@router.get("/", response_model=List[HabitLogRead])
def read_logs(db: Session = Depends(get_db)):
    try:
        logs = db.query(HabitLog).order_by(HabitLog.date.desc()).all()
        print(f"✅ {len(logs)} log(s) d’habitudes récupérés")
        return logs
    except Exception as e:
        print(f"❌ ERREUR read_logs: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des logs")

# Créer un log
@router.post("/", response_model=HabitLogRead)
def create_log(log: HabitLogCreate, db: Session = Depends(get_db)):
    try:
        db_log = HabitLog(**log.dict())
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        return db_log
    except Exception as e:
        print("❌ Erreur create_log:", e)
        raise HTTPException(status_code=500, detail="Erreur lors de la création du log")

# Modifier un log
@router.put("/{log_id}", response_model=HabitLogRead)
def update_log(log_id: int, log: HabitLogUpdate, db: Session = Depends(get_db)):
    db_log = db.query(HabitLog).filter(HabitLog.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Log introuvable")
    for key, value in log.dict(exclude_unset=True).items():
        setattr(db_log, key, value)
    db.commit()
    db.refresh(db_log)
    return db_log

# Supprimer un log
@router.delete("/{log_id}")
def delete_log(log_id: int, db: Session = Depends(get_db)):
    db_log = db.query(HabitLog).filter(HabitLog.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Log introuvable")
    db.delete(db_log)
    db.commit()
    return {"detail": "Log supprimé"}
