"""
Vector API Router.

Provides endpoint for inserting document chunks with embeddings.
Used by ingestion service after processing documents.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.db import get_db
from ..models.query import (
    VectorInsertRequest,
    VectorInsertResponse,
    ErrorResponse
)
from ..services import vector_service


router = APIRouter(prefix="/vector", tags=["Vector Operations"])


@router.post(
    "/insert",
    response_model=VectorInsertResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Insert a document chunk",
    description="Insert a text chunk with its vector embedding into the database"
)
async def insert_vector(
    request: VectorInsertRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Insert a document chunk with embedding.
    
    This endpoint is called by the ingestion service after:
    1. Document parsing
    2. Text chunking
    3. Embedding generation
    
    The chunk is stored in PostgreSQL with pgvector for efficient similarity search.
    """
    try:
        chunk = await vector_service.insert_chunk(
            db=db,
            chunk_id=request.id,
            user_id=request.user_id,
            text=request.text,
            embedding=request.embedding,
            metadata=request.metadata
        )
        
        return VectorInsertResponse(
            status="ok",
            id=str(chunk.id)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "InsertError",
                "message": str(e)
            }
        )
