"""
Vector Service for RAG.

This service handles vector storage operations:
- Inserting chunks with embeddings into PostgreSQL/pgvector
- Bulk insert operations
"""

from typing import Dict, Any, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.chunk import DocumentChunk


async def insert_chunk(
    db: AsyncSession,
    chunk_id: UUID,
    user_id: str,
    text: str,
    embedding: list,
    metadata: Optional[Dict[str, Any]] = None
) -> DocumentChunk:
    """
    Insert a single chunk with its embedding into the database.
    
    Args:
        db: Database session
        chunk_id: Unique identifier for the chunk
        user_id: Owner of the chunk
        text: Original text content
        embedding: Vector embedding (768 floats)
        metadata: Optional metadata dict
        
    Returns:
        Created DocumentChunk instance
    """
    chunk = DocumentChunk(
        id=chunk_id,
        user_id=user_id,
        text=text,
        embedding=embedding,
        chunk_metadata=metadata or {}
    )
    
    db.add(chunk)
    await db.flush()  # Get the ID without committing
    await db.refresh(chunk)
    
    return chunk


async def insert_chunks_bulk(
    db: AsyncSession,
    chunks: list[Dict[str, Any]]
) -> list[DocumentChunk]:
    """
    Insert multiple chunks in a single transaction.
    
    More efficient for batch ingestion.
    
    Args:
        db: Database session
        chunks: List of dicts with keys: id, user_id, text, embedding, metadata
        
    Returns:
        List of created DocumentChunk instances
    """
    chunk_objects = [
        DocumentChunk(
            id=c["id"],
            user_id=c["user_id"],
            text=c["text"],
            embedding=c["embedding"],
            chunk_metadata=c.get("metadata", {})
        )
        for c in chunks
    ]
    
    db.add_all(chunk_objects)
    await db.flush()
    
    return chunk_objects


async def get_chunk_by_id(
    db: AsyncSession,
    chunk_id: UUID
) -> Optional[DocumentChunk]:
    """
    Retrieve a chunk by its ID.
    
    Args:
        db: Database session
        chunk_id: UUID of the chunk
        
    Returns:
        DocumentChunk or None if not found
    """
    return await db.get(DocumentChunk, chunk_id)


async def delete_chunk(
    db: AsyncSession,
    chunk_id: UUID
) -> bool:
    """
    Delete a chunk by its ID.
    
    Args:
        db: Database session
        chunk_id: UUID of the chunk to delete
        
    Returns:
        True if deleted, False if not found
    """
    chunk = await db.get(DocumentChunk, chunk_id)
    if chunk:
        await db.delete(chunk)
        return True
    return False
