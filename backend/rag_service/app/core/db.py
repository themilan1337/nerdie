"""
Database module for RAG Service.

This module provides:
- Async SQLAlchemy engine and session factory
- pgvector extension initialization
- Database session dependency for FastAPI
- Table creation utilities

Uses SQLAlchemy 2.0+ async patterns.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import declarative_base
from sqlalchemy import text

from .config import get_settings


# Get settings
settings = get_settings()

# ===== SQLAlchemy Engine =====
# Create async engine with connection pooling
engine = create_async_engine(
    settings.database_url,
    echo=False,  # Set to True for SQL query logging
    pool_pre_ping=True,  # Verify connections before using
    pool_size=10,
    max_overflow=20
)

# ===== Session Factory =====
# async_sessionmaker creates async sessions for each request
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Don't expire objects after commit
    autoflush=False
)

# ===== Base Model =====
# All SQLAlchemy models inherit from this
Base = declarative_base()


async def init_db() -> None:
    """
    Initialize database on startup.
    
    This function:
    1. Creates pgvector extension if not exists
    2. Creates all tables defined in models
    
    Should be called during application lifespan startup.
    """
    async with engine.begin() as conn:
        # Create pgvector extension for vector similarity search
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        
        # Import models to register them with Base
        from ..models.chunk import DocumentChunk  # noqa: F401
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Database initialized with pgvector extension")


async def close_db() -> None:
    """
    Close database connections on shutdown.
    Disposes of the connection pool.
    """
    await engine.dispose()
    print("👋 Database connections closed")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session.
    
    Usage in FastAPI:
        @router.post("/endpoint")
        async def endpoint(db: AsyncSession = Depends(get_db)):
            ...
    
    The session is automatically closed after the request.
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@asynccontextmanager
async def get_db_context() -> AsyncGenerator[AsyncSession, None]:
    """
    Context manager for database sessions.
    
    Usage in services:
        async with get_db_context() as db:
            ...
    
    Useful when not using FastAPI dependency injection.
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
