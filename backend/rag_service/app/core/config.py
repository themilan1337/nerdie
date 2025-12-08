"""
Configuration module for RAG Service.

This module loads all environment variables needed for:
- PostgreSQL connection (with pgvector)
- Google Gemini API
- CORS settings
"""

from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    All values can be overridden via .env file or environment.
    """
    
    # ===== PostgreSQL Configuration =====
    # Connection string for async SQLAlchemy
    postgres_user: str = "nerdie"
    postgres_password: str = "nerdie_password"
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_db: str = "nerdie_rag"
    
    @property
    def database_url(self) -> str:
        """Async PostgreSQL connection string for SQLAlchemy."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
    
    @property
    def sync_database_url(self) -> str:
        """Sync PostgreSQL connection string (for Alembic migrations)."""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
    
    # ===== Gemini API Configuration =====
    gemini_api_key: str
    gemini_embedding_model: str = "text-embedding-004"
    gemini_llm_model: str = "gemini-1.5-flash"
    
    # ===== Vector Search Configuration =====
    # Dimension of embedding vectors (Gemini text-embedding-004 uses 768)
    embedding_dimension: int = 768
    # Number of top results to return in similarity search
    top_k: int = 5
    # Maximum distance threshold for relevance (lower = more similar)
    max_distance: float = 1.0
    
    # ===== CORS Configuration =====
    cors_origins: str = "http://localhost:3000"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Using lru_cache to avoid re-reading .env on every request.
    """
    return Settings()
