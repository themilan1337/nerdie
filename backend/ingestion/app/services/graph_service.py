"""
Knowledge Graph extraction service.

Uses Gemini to extract entities and relations from text chunks.
"""

import json
from typing import List, Dict, Any
import google.generativeai as genai
from ..core.config import get_settings

settings = get_settings()

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)


EXTRACTION_PROMPT = """Extract entities and relations from this text.

Return ONLY valid JSON in this exact format:
{
  "entities": ["entity1", "entity2", ...],
  "relations": [
    {"source": "entity1", "target": "entity2", "type": "relation_type"}
  ]
}

Rules:
- Entities should be nouns, concepts, people, places, organizations
- Relations describe how entities are connected
- Keep entity names short and normalized (lowercase)
- Common relation types: "is_a", "has", "relates_to", "part_of", "created_by", "located_in"

Text to analyze:
{text}

JSON response:"""


class GraphExtractionService:
    def __init__(self):
        self.model = genai.GenerativeModel(settings.GEMINI_LLM_MODEL)
    
    async def extract_graph(self, text: str) -> Dict[str, Any]:
        """
        Extract entities and relations from text using Gemini.
        
        Args:
            text: Text chunk to analyze
            
        Returns:
            Dict with 'entities' list and 'relations' list
        """
        try:
            prompt = EXTRACTION_PROMPT.format(text=text[:2000])  # Limit text length
            
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,  # Low temperature for structured output
                    max_output_tokens=1024,
                )
            )
            
            # Parse JSON response
            response_text = response.text.strip()
            
            # Handle markdown code blocks
            if response_text.startswith("```"):
                lines = response_text.split("\n")
                response_text = "\n".join(lines[1:-1])
            
            result = json.loads(response_text)
            
            return {
                "entities": result.get("entities", []),
                "relations": result.get("relations", [])
            }
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse graph extraction response: {e}")
            return {"entities": [], "relations": []}
        except Exception as e:
            print(f"Graph extraction error: {e}")
            return {"entities": [], "relations": []}
    
    async def extract_from_chunks(self, chunks: List[str]) -> Dict[str, Any]:
        """
        Extract graph from multiple chunks and merge results.
        
        Args:
            chunks: List of text chunks
            
        Returns:
            Merged entities and relations
        """
        all_entities = set()
        all_relations = []
        
        for chunk in chunks[:5]:  # Limit to first 5 chunks for performance
            result = await self.extract_graph(chunk)
            all_entities.update(result.get("entities", []))
            all_relations.extend(result.get("relations", []))
        
        # Deduplicate relations
        unique_relations = []
        seen = set()
        for rel in all_relations:
            key = (rel.get("source"), rel.get("target"), rel.get("type"))
            if key not in seen:
                seen.add(key)
                unique_relations.append(rel)
        
        return {
            "entities": list(all_entities),
            "relations": unique_relations
        }


graph_extraction_service = GraphExtractionService()
