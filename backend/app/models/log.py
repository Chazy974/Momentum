from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    habit_id = Column(Integer, ForeignKey("habits.id", ondelete="CASCADE"))
    timestamp = Column(DateTime, default=datetime.utcnow)

    # 🔁 Ici on peut utiliser la classe directement
    habit = relationship("Habit", back_populates="logs")
