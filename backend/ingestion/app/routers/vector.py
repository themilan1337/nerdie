from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session

from ..core.database import get_db, TextChunk

router = APIRouter(
    prefix="/vector",
    tags=["Vector"]
)

class VectorInsertInput(BaseModel):
    text: str
    embedding: List[float]
    metadata: Optional[dict] = {}
    source: Optional[str] = "manual_insert"

@router.post("/insert")
async def insert_vector(input: VectorInsertInput, db: Session = Depends(get_db)):
    """
    Directly insert a text chunk and its embedding into the vector database.
    Useful for testing or manual insertion.
    """
    try:
        db_chunk = TextChunk(
            content=input.text,
            embedding=input.embedding,
            metadata_=input.metadata,
            source=input.source
        )
        db.add(db_chunk)
        db.commit()
        db.refresh(db_chunk)
        
        return {
            "status": "success",
            "id": db_chunk.id,
            "message": "Vector inserted successfully"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
