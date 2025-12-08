"""
Pydantic schemas for RAG API requests and responses.

These schemas define the contract for:
- Vector insertion endpoint
- RAG query endpoint
- Response formats
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from uuid import UUID


# ========================================
# Vector Insert Schemas
# ========================================

class VectorInsertRequest(BaseModel):
    """
    Request schema for inserting a chunk with its embedding.
    
    Used by ingestion service to store processed chunks.
    """
    id: UUID = Field(..., description="Unique identifier for the chunk")
    user_id: str = Field(..., description="User ID for multi-tenant isolation")
    text: str = Field(..., description="Original text content")
    embedding: List[float] = Field(..., description="Vector embedding (768 dims)")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional metadata (source, page, etc.)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "user123",
                "text": "The quick brown fox jumps over the lazy dog.",
                "embedding": [0.1, 0.2, 0.3],  # Truncated for example
                "metadata": {
                    "source": "document.pdf",
                    "page": 1,
                    "chunk_index": 0
                }
            }
        }


class VectorInsertResponse(BaseModel):
    """Response schema for successful vector insertion."""
    status: str = "ok"
    id: str


# ========================================
# RAG Query Schemas
# ========================================

class RAGQueryRequest(BaseModel):
    """
    Request schema for RAG query.
    
    The query will be:
    1. Embedded using Gemini
    2. Used for similarity search
    3. Context assembled and sent to LLM
    """
    query: str = Field(..., description="User's question")
    user_id: str = Field(..., description="User ID to filter chunks")
    top_k: Optional[int] = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of chunks to retrieve"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is the main topic of the document?",
                "user_id": "user123",
                "top_k": 5
            }
        }


class ChunkResult(BaseModel):
    """
    A single chunk result from similarity search.
    
    Supports both text and image chunks:
    - type="text": regular text chunk
    - type="image": image chunk with image_url
    """
    id: str
    text: str
    metadata: Optional[Dict[str, Any]]
    score: float = Field(..., description="Similarity score (lower = more similar)")
    # Image support fields
    type: str = Field(default="text", description="Chunk type: 'text' or 'image'")
    image_url: Optional[str] = Field(default=None, description="Image URL if type='image'")


class RAGQueryResponse(BaseModel):
    """
    Response schema for RAG query.
    
    Includes:
    - Generated answer from LLM
    - Retrieved chunks with scores
    - Full context that was used
    """
    answer: str = Field(..., description="LLM-generated answer based on context")
    chunks: List[ChunkResult] = Field(..., description="Retrieved relevant chunks")
    context_used: str = Field(..., description="Full context sent to LLM")
    scores: List[float] = Field(..., description="Similarity scores for each chunk")


# ========================================
# Error Schemas
# ========================================

class ErrorResponse(BaseModel):
    """Standard error response format."""
    error: str
    message: str


# ========================================
# Health Check
# ========================================

class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "ok"
    service: str = "rag_service"
    database: str = "connected"


# ========================================
# Graph Query Schemas (MVP)
# ========================================

class GraphNode(BaseModel):
    """A node in the knowledge graph."""
    id: str
    label: str
    type: str
    properties: Optional[Dict[str, Any]] = None


class GraphEdge(BaseModel):
    """An edge in the knowledge graph."""
    source: str
    target: str
    relation: str
    properties: Optional[Dict[str, Any]] = None


class GraphQueryResponse(BaseModel):
    """Response schema for graph query (MVP stub)."""
    entity: str
    nodes: List[GraphNode] = Field(default_factory=list)
    edges: List[GraphEdge] = Field(default_factory=list)
