import google.generativeai as genai
from typing import List, Dict, Any
from ..core.config import get_settings

settings = get_settings()

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

class EmbeddingService:
    def __init__(self):
        self.model = settings.GEMINI_EMBEDDING_MODEL

    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text chunk."""
        try:
            result = genai.embed_content(
                model=self.model,
                content=text,
                task_type="retrieval_document",
                title="Embedding of text chunk"
            )
            return result['embedding']
        except Exception as e:
            print(f"Error generating embedding: {e}")
            raise e

    def chunk_text(self, text: str, chunk_size: int = 300) -> List[str]:
        """
        Split text into chunks of approximately chunk_size words.
        Simple implementation - can be enhanced with overlap or sentence splitting.
        """
        words = text.split()
        chunks = []
        current_chunk = []
        current_count = 0
        
        for word in words:
            current_chunk.append(word)
            current_count += 1
            
            if current_count >= chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_count = 0
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
            
        return chunks

embedding_service = EmbeddingService()
