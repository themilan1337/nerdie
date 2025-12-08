"""
Gemini API Client for RAG Service.

This module provides integration with Google's Gemini API for:
1. Text embeddings (text-embedding-004)
2. LLM generation (gemini-2.5-flash)

Uses the official google-generativeai SDK.
"""

from typing import List
import google.generativeai as genai

from ..core.config import get_settings


# Get settings
settings = get_settings()

# Configure Gemini with API key
genai.configure(api_key=settings.gemini_api_key)


# ========================================
# Anti-Hallucination System Prompt
# ========================================

RAG_SYSTEM_PROMPT = """You are a helpful assistant that answers questions based ONLY on the provided context.

CRITICAL RULES:
1. You must ONLY use information from the PROVIDED CONTEXT below.
2. If the context does not contain enough information to answer the question, respond EXACTLY with: "Information not found in the knowledge base."
3. Do NOT make up information or use external knowledge.
4. Always cite which part of the context your answer is based on.
5. Be concise and accurate.

CONTEXT:
{context}

USER QUESTION: {query}

ANSWER (based strictly on the context above):"""


async def generate_embedding(text: str) -> List[float]:
    """
    Generate embedding vector for text using Gemini.
    
    Uses text-embedding-004 model which outputs 768-dimensional vectors.
    
    Args:
        text: Text to embed (max ~2048 tokens recommended)
        
    Returns:
        List of 768 floats representing the embedding
        
    Raises:
        Exception: If embedding generation fails
    """
    try:
        result = genai.embed_content(
            model=f"models/{settings.gemini_embedding_model}",
            content=text,
            task_type="retrieval_document"  # Optimized for document retrieval
        )
        return result['embedding']
    except Exception as e:
        raise Exception(f"Embedding generation failed: {str(e)}")


async def generate_query_embedding(query: str) -> List[float]:
    """
    Generate embedding for a search query.
    
    Uses task_type="retrieval_query" for better query-document matching.
    
    Args:
        query: Search query text
        
    Returns:
        List of 768 floats representing the query embedding
    """
    try:
        result = genai.embed_content(
            model=f"models/{settings.gemini_embedding_model}",
            content=query,
            task_type="retrieval_query"  # Optimized for query matching
        )
        return result['embedding']
    except Exception as e:
        raise Exception(f"Query embedding generation failed: {str(e)}")


async def generate_answer(query: str, context: str) -> str:
    """
    Generate an answer using Gemini LLM based on provided context.
    
    Uses anti-hallucination prompt to ensure answers are grounded
    in the provided context only.
    
    Args:
        query: User's question
        context: Retrieved context from vector search
        
    Returns:
        Generated answer string
        
    Raises:
        Exception: If generation fails
    """
    try:
        # Create the model
        model = genai.GenerativeModel(
            model_name=settings.gemini_llm_model,
            generation_config={
                "temperature": 0.3,  # Low temperature for factual responses
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 1024,
            }
        )
        
        # Format prompt with context and query
        prompt = RAG_SYSTEM_PROMPT.format(
            context=context,
            query=query
        )
        
        # Generate response
        response = model.generate_content(prompt)
        
        # Extract text from response
        if response.parts:
            return response.text
        else:
            return "Information not found in the knowledge base."
            
    except Exception as e:
        raise Exception(f"Answer generation failed: {str(e)}")


async def generate_answer_with_sources(
    query: str,
    chunks: List[dict]
) -> str:
    """
    Generate answer with explicit source references.
    
    Enhanced version that includes source metadata in the response.
    
    Args:
        query: User's question
        chunks: List of chunk dicts with 'text' and 'metadata'
        
    Returns:
        Generated answer with source references
    """
    # Build context with source labels
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        source = chunk.get("metadata", {}).get("source", f"Source {i}")
        context_parts.append(f"[{source}]: {chunk['text']}")
    
    context = "\n\n".join(context_parts)
    
    return await generate_answer(query, context)
