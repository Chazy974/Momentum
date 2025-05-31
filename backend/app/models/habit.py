from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime
import enum
class HabitTargetType(enum.Enum):
    boolean = "boolean"
    numeric = "numeric"
    time = "time"
class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="habits")
    
    habit_logs = relationship("HabitLog", back_populates="habit")  
