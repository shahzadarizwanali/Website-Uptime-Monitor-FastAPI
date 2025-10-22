import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel
from alembic import context

# --- Ensure Alembic can find your app package ---
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# --- Import models so Alembic can detect them ---
from app.models.website import Website, WebsiteCheck
from app.core.config import settings

# --- Alembic Config object (reads alembic.ini) ---
config = context.config

# --- Set up logging ---git
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Convert async DB URL (aiosqlite) -> sync URL for Alembic ---
db_url = settings.DATABASE_URL.replace("+aiosqlite", "")
config.set_main_option("sqlalchemy.url", db_url)

# --- Tell Alembic which metadata to use ---
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
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
