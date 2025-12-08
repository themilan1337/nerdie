"""
RAG Query API Router.

Provides the main RAG query endpoint that:
1. Takes a user question
2. Searches for relevant context
3. Generates an answer using Gemini
4. Returns answer with sources
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.db import get_db
from ..models.query import (
    RAGQueryRequest,
    RAGQueryResponse,
    ChunkResult,
    ErrorResponse
)
from ..services import rag_service


router = APIRouter(prefix="/rag", tags=["RAG Query"])


@router.post(
    "/query",
    response_model=RAGQueryResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Query the knowledge base",
    description="Ask a question and get an AI-generated answer based on your documents"
)
async def rag_query(
    request: RAGQueryRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Execute RAG query pipeline.
    
    Pipeline:
    1. Embed the query using Gemini text-embedding-004
    2. Search for similar chunks in the user's knowledge base
    3. Assemble context from top-K relevant chunks
    4. Generate answer using Gemini LLM with anti-hallucination prompt
    
    The answer will ONLY contain information from the knowledge base.
    If no relevant data is found, returns "Information not found in the knowledge base."
    """
    try:
        result = await rag_service.rag_query(
            db=db,
            query=request.query,
            user_id=request.user_id,
            top_k=request.top_k or 5
        )
        
        # Convert to response model with image support
        chunks = [
            ChunkResult(
                id=c["id"],
                text=c["text"],
                metadata=c["metadata"],
                score=c["score"],
                type=c.get("type", "text"),
                image_url=c.get("image_url")
            )
            for c in result["chunks"]
        ]
        
        return RAGQueryResponse(
            answer=result["answer"],
            chunks=chunks,
            context_used=result["context_used"],
            scores=result["scores"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "RAGQueryError",
                "message": str(e)
            }
        )
