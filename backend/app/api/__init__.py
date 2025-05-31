from fastapi import APIRouter
from . import tasks, habits, habit_logs

api_router = APIRouter()
api_router.include_router(tasks.router)
api_router.include_router(habits.router)
api_router.include_router(habit_logs.router)