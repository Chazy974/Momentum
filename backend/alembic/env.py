from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# Ajoute le dossier parent à sys.path pour permettre les imports relatifs
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.config import settings
from app.models.base import Base
import app.models  # important pour que tous les modèles soient bien pris en compte

# Configuration Alembic
config = context.config

# Ne pas injecter l'URL avec set_main_option car elle contient un %
# On la passera manuellement dans run_migrations_online/offline
DB_URL = str(settings.SQLALCHEMY_DATABASE_URL)

# Configuration du logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Cible : métadonnées SQLAlchemy
target_metadata = Base.metadata

def run_migrations_offline():
    """Mode offline : génère le SQL sans connexion directe à la BDD"""
    context.configure(
        url=DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Mode online : exécute les migrations avec connexion active"""
    connectable = engine_from_config(
        {"sqlalchemy.url": DB_URL},  # ← On injecte ici, sans toucher à config.set_main_option
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
