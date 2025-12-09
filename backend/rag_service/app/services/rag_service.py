"""
RAG Service - Core Retrieval-Augmented Generation Logic.

This is the main service that orchestrates the RAG pipeline:
1. Embed the user query
2. Perform similarity search in pgvector
3. Assemble context from retrieved chunks
4. Generate answer using Gemini LLM

The pipeline ensures answers are grounded in the knowledge base.
"""

from typing import List, Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import JSONB

from ..core.config import get_settings
from ..models.chunk import DocumentChunk
from . import gemini_client


settings = get_settings()


async def similarity_search(
    db: AsyncSession,
    query_embedding: List[float],
    user_id: str,
    top_k: int = 5,
    max_distance: float = 1.0
) -> List[Tuple[DocumentChunk, float]]:
    """
    Perform similarity search using pgvector.
    
    Uses cosine distance (<->) for similarity ranking.
    Lower distance = more similar.
    
    Args:
        db: Database session
        query_embedding: Query vector (768 dims)
        user_id: Filter chunks by user
        top_k: Number of results to return
        max_distance: Maximum distance threshold
        
    Returns:
        List of (DocumentChunk, distance) tuples
    """
    # Convert embedding to pgvector format
    embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"

    # SQL query with pgvector similarity search
    # Using <-> operator for cosine distance
    # IMPORTANT: .columns(metadata=JSONB) ensures JSONB is properly deserialized
    query = text("""
        SELECT
            id,
            user_id,
            text,
            metadata,
            created_at,
            embedding <-> :query_embedding AS distance
        FROM document_chunks
        WHERE user_id = :user_id
        AND embedding <-> :query_embedding < :max_distance
        ORDER BY embedding <-> :query_embedding
        LIMIT :top_k
    """).columns(metadata=JSONB)
    
    result = await db.execute(
        query,
        {
            "query_embedding": embedding_str,
            "user_id": user_id,
            "max_distance": max_distance,
            "top_k": top_k
        }
    )
    
    rows = result.fetchall()
    
    # Convert to DocumentChunk objects with distances
    chunks_with_scores = []
    for row in rows:
        # JSONB metadata is now properly deserialized thanks to .columns(metadata=JSONB)
        metadata = row.metadata if row.metadata else {}

        chunk = DocumentChunk(
            id=row.id,
            user_id=row.user_id,
            text=row.text,
            chunk_metadata=metadata,
            created_at=row.created_at
        )
        chunks_with_scores.append((chunk, row.distance))

    return chunks_with_scores


def assemble_context(chunks: List[DocumentChunk]) -> str:
    """
    Assemble retrieved chunks into a single context string.
        Formatted context string
    """
    if not chunks:
        return "No relevant documents found."
    
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        # Extract source info from metadata
        metadata = chunk.chunk_metadata or {}
        source = metadata.get("source", f"Document {i}")
        page = metadata.get("page")
        
        # Format source reference
        if page:
            source_ref = f"[Source: {source}, Page {page}]"
        else:
            source_ref = f"[Source: {source}]"
        
        context_parts.append(f"{source_ref}\n{chunk.text}")
    
    return "\n\n---\n\n".join(context_parts)


async def rag_query(
    db: AsyncSession,
    query: str,
    user_id: str,
    top_k: int = 10,
) -> Dict[str, Any]:
    """
    Execute full RAG pipeline.
    
    Pipeline steps:
    1. Generate embedding for query using Gemini
    2. Search for similar chunks in user's knowledge base
    3. Assemble context from retrieved chunks
    4. Generate answer using Gemini LLM with anti-hallucination prompt
    5. Return answer with sources and scores
    
    Args:
        db: Database session
        query: User's question
        user_id: User ID for filtering chunks
        top_k: Number of chunks to retrieve
        
    Returns:
        Dict with answer, chunks, context_used, and scores
    """
import logging

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def rag_query(
    db: AsyncSession,
    query: str,
    user_id: str,
    top_k: int = 10,
) -> Dict[str, Any]:
    """
    Execute full RAG pipeline.
    """
    # Step 1: Generate query embedding
    logger.info(f"Generating embedding for query: {query}")
    query_embedding = await gemini_client.generate_query_embedding(query)
    
    # Step 2: Similarity search
    logger.info(f"Performing similarity search with top_k={top_k}")
    chunks_with_scores = await similarity_search(
        db=db,
        query_embedding=query_embedding,
        user_id=user_id,
        top_k=top_k
    )
    
    # Extract chunks and scores
    chunks = [c for c, _ in chunks_with_scores]
    scores = [s for _, s in chunks_with_scores]
    
    logger.info(f"Retrieved {len(chunks)} chunks. Scores: {scores}")
    
    # Step 3: Check if we found relevant context
    if not chunks:
        logger.info("No chunks found.")
        return {
            "answer": "No relevant data found in the knowledge base.",
            "chunks": [],
            "context_used": "",
            "scores": []
        }
    
    # Step 4: Assemble context
    context = assemble_context(chunks)
    logger.info(f"Assembled context length: {len(context)} chars")
    
    # Step 5: Generate answer with Gemini
    logger.info("Generating answer with Gemini...")
    answer = await gemini_client.generate_answer(query, context)
    logger.info(f"Generated answer: {answer[:100]}...")
    
    # Step 6: Format response with image support
    chunk_results = []
    for chunk, score in chunks_with_scores:
        metadata = chunk.chunk_metadata or {}
        chunk_type = metadata.get("type", "text")
        image_url = metadata.get("image_url") if chunk_type == "image" else None
        
        chunk_results.append({
            "id": str(chunk.id),
            "text": chunk.text,
            "metadata": metadata,
            "score": score,
            "type": chunk_type,
            "image_url": image_url
        })
    
    return {
        "answer": answer,
        "chunks": chunk_results,
        "context_used": context,
        "scores": scores
    }


async def rag_query_with_threshold(
    db: AsyncSession,
    query: str,
    user_id: str,
    top_k: int = 10,
    score_threshold: float = 0.5
) -> Dict[str, Any]:
    """
    RAG query with additional score filtering.
    
    Only includes chunks that meet the similarity threshold.
    Useful for avoiding low-relevance context pollution.
    
    Args:
        db: Database session
        query: User's question
        user_id: User ID
        top_k: Maximum chunks to retrieve
        score_threshold: Maximum distance to include
        
    Returns:
        Same as rag_query but filtered by threshold
    """
    # Generate query embedding
    query_embedding = await gemini_client.generate_query_embedding(query)
    
    # Search with threshold
    chunks_with_scores = await similarity_search(
        db=db,
        query_embedding=query_embedding,
        user_id=user_id,
        top_k=top_k,
        max_distance=score_threshold
    )
    
    chunks = [c for c, _ in chunks_with_scores]
    scores = [s for _, s in chunks_with_scores]
    
    if not chunks:
        return {
            "answer": "No sufficiently relevant data found in the knowledge base.",
            "chunks": [],
            "context_used": "",
            "scores": []
        }
    
    context = assemble_context(chunks)
    answer = await gemini_client.generate_answer(query, context)
    
    # Format response with image support
    chunk_results = []
    for chunk, score in chunks_with_scores:
        metadata = chunk.chunk_metadata or {}
        logger.info(f"Chunk {chunk.id} metadata: {metadata}")  # Debug log
        
        chunk_type = metadata.get("type", "text")
        image_url = metadata.get("image_url") if chunk_type == "image" else None
        
        chunk_results.append({
            "id": str(chunk.id),
            "text": chunk.text,
            "metadata": metadata,
            "score": score,
            "type": chunk_type,
            "image_url": image_url
        })
    
    return {
        "answer": answer,
        "chunks": chunk_results,
        "context_used": context,
        "scores": scores
    }
