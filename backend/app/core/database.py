from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from ..models.base import Base  # <- utilise ta base déclarée

# 👉 À adapter selon ton cas
DB_USER = "postgres"
DB_PASSWORD = "ton_mot_de_passe"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "momentum"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
