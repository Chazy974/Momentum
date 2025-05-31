from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate, TaskOut
from typing import List

router = APIRouter(prefix="/tasks", tags=["tasks"])

# Dépendance DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Lire toutes les tâches
@router.get("/", response_model=List[TaskRead])
def read_tasks(db: Session = Depends(get_db)):
    try:
        tasks = db.query(Task).order_by(Task.completed.asc(), Task.due_date.asc()).all()
        print(f"✅ {len(tasks)} tâche(s) récupérées")
        return tasks
    except Exception as e:
        print(f"❌ ERREUR read_tasks: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des tâches")

# Créer une tâche
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

# Modifier une tâche
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

# Supprimer une tâche
@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted"}
