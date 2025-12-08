"""
SQLAlchemy model for document chunks.

This model represents vectorized text chunks stored in PostgreSQL with pgvector.
Each chunk belongs to a user and contains:
- The original text
- Vector embedding (768 dimensions for Gemini text-embedding-004)
- Metadata (source file, page number, etc.)
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pgvector.sqlalchemy import Vector

from ..core.db import Base
from ..core.config import get_settings


settings = get_settings()


class DocumentChunk(Base):
    """
    Represents a chunk of text with its vector embedding.
    
    This is the core table for RAG vector search.
    Uses pgvector for efficient similarity search.
    
    Attributes:
        id: Unique identifier (UUID)
        user_id: Owner of the chunk (for multi-tenant isolation)
        text: Original text content of the chunk
        embedding: Vector representation (768 dims for Gemini)
        metadata: JSON object with source info, page numbers, etc.
        created_at: Timestamp of insertion
    """
    
    __tablename__ = "document_chunks"
    
    # Primary key - UUID for distributed systems compatibility
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )
    
    # User isolation - each user sees only their chunks
    user_id = Column(
        String(255),
        nullable=False,
        index=True  # Index for fast user filtering
    )
    
    # Original text content
    text = Column(
        Text,
        nullable=False
    )
    
    # Vector embedding for similarity search
    # Dimension must match the embedding model output
    embedding = Column(
        Vector(settings.embedding_dimension),
        nullable=False
    )
    
    # Flexible metadata storage
    # Can include: source_file, page_number, chunk_index, etc.
    metadata = Column(
        JSONB,
        nullable=True,
        default=dict
    )
    
    # Audit timestamp
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    def __repr__(self) -> str:
        return f"<DocumentChunk(id={self.id}, user_id={self.user_id})>"
    
    def to_dict(self) -> dict:
        """Convert model to dictionary for API responses."""
        return {
            "id": str(self.id),
            "user_id": self.user_id,
            "text": self.text,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
