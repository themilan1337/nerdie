"""
Configuration module for the Auth microservice.
Loads environment variables using pydantic-settings.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Firebase Configuration
    firebase_project_id: str
    firebase_api_key: str
    firebase_credentials: str = "./firebase-credentials.json"
    
    # Server Configuration
    cors_origins: str = "http://localhost:3000"
    
    # API Configuration
    api_prefix: str = "/auth"
    
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
    """Get cached settings instance."""
    return Settings()
