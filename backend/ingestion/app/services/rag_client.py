"""
RAG Service client for cross-service communication.

Sends processed chunks to rag_service for vector storage.
"""

import httpx
from typing import Dict, Any, List, Optional
import uuid
from ..core.config import get_settings

settings = get_settings()


class RAGServiceClient:
    def __init__(self):
        self.base_url = settings.RAG_SERVICE_URL
        self.timeout = 30.0
    
    async def insert_chunk(
        self,
        user_id: str,
        text: str,
        embedding: List[float],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Insert a single chunk into rag_service vector store.
        
        Args:
            user_id: Owner of the chunk
            text: Text content
            embedding: Vector embedding
            metadata: Optional metadata dict
            
        Returns:
            Response from rag_service
        """
        chunk_id = str(uuid.uuid4())
        
        payload = {
            "id": chunk_id,
            "user_id": user_id,
            "text": text,
            "embedding": embedding,
            "metadata": metadata or {}
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/vector/insert",
                    json=payload
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"Error inserting chunk to rag_service: {e}")
                raise
    
    async def insert_chunks_batch(
        self,
        user_id: str,
        chunks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Insert multiple chunks into rag_service.
        
        Args:
            user_id: Owner of the chunks
            chunks: List of dicts with 'text', 'embedding', 'metadata'
            
        Returns:
            List of responses
        """
        results = []
        
        for chunk in chunks:
            result = await self.insert_chunk(
                user_id=user_id,
                text=chunk["text"],
                embedding=chunk["embedding"],
                metadata=chunk.get("metadata", {})
            )
            results.append(result)
        
        return results


rag_client = RAGServiceClient()
