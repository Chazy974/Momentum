from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Lié aux tâches
    tasks = relationship("Task", back_populates="user", cascade="all, delete")
    habits = relationship("Habit", back_populates="user", cascade="all, delete")
