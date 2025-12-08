"""
Alembic env.py - Migration environment configuration.

This file configures Alembic to work with our async SQLAlchemy setup.
"""

from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy import create_engine

from alembic import context

# Import our models and config
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import get_settings
from app.core.db import Base
from app.models.chunk import DocumentChunk  # noqa: F401

# Alembic Config object
config = context.config

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for autogenerate
target_metadata = Base.metadata

# Get database URL
settings = get_settings()


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    
    Configures the context with just a URL and not an Engine.
    Calls to context.execute() emit the SQL to the script output.
    """
    url = settings.sync_database_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    
    Creates an Engine and associates a connection with the context.
    """
    connectable = create_engine(
        settings.sync_database_url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
