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
                title="Embedding of text chunk",
                output_dimensionality=768  # Use 768 dimensions for storage efficiency
            )
            return result['embedding']
        except Exception as e:
            print(f"Error generating embedding: {e}")
            raise e

    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
        """
        Split text into chunks with overlap for better context preservation.
        
        Uses character-based splitting with sentence boundary awareness.
        
        Args:
            text: Text to split
            chunk_size: Target size in characters (default 500)
            overlap: Overlap between chunks in characters (default 100)
            
        Returns:
            List of text chunks
        """
        if not text or len(text) < chunk_size:
            return [text] if text else []
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            # Find end position
            end = start + chunk_size
            
            if end >= text_length:
                # Last chunk
                chunks.append(text[start:].strip())
                break
            
            # Try to break at sentence boundary
            best_break = end
            for boundary in ['. ', '.\n', '! ', '? ', '\n\n', '\n']:
                pos = text.rfind(boundary, start + chunk_size // 2, end)
                if pos != -1:
                    best_break = pos + len(boundary)
                    break
            
            chunk = text[start:best_break].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start with overlap
            start = best_break - overlap if best_break > overlap else best_break
        
        return chunks

embedding_service = EmbeddingService()

