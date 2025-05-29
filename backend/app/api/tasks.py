from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.task import Task
from app.models.user import User  # pour futur lien avec utilisateur
from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime
from dateutil.parser import parse as dateutil_parse

router = APIRouter(prefix="/tasks", tags=["tasks"])

# Dépendance
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schémas Pydantic
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

class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: bool

    class Config:
        from_attributes = True

# Routes
@router.get("/", response_model=List[TaskOut])
def read_tasks(db: Session = Depends(get_db)):
    print(">>> GET /tasks appelé")
    try:
        tasks = db.query(Task).all()
        return tasks
    except Exception as e:
        print(f"❌ ERREUR read_tasks: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=TaskOut)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    try:
        print("🔥 Données reçues:", task.dict())
        db_task = Task(**task.dict(), user_id=None)  # utilisateur non encore géré
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        print("❌ Erreur create_task:", e)
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Erreur lors de la création")

@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted"}
