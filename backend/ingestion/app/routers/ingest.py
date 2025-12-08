from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session

from ..core.database import get_db, TextChunk
from ..services.embedding_service import embedding_service
from ..services.storage_service import storage_service
from ..services.processing_service import processing_service

router = APIRouter(
    prefix="/ingest",
    tags=["Ingestion"]
)

class TextInput(BaseModel):
    text: str
    metadata: Optional[dict] = {}

@router.post("/text")
async def ingest_text(input: TextInput, db: Session = Depends(get_db)):
    """
    Ingest raw text, chunk it, generate embeddings, and store in vector DB.
    """
    try:
        # 1. Chunk text
        chunks = embedding_service.chunk_text(input.text)
        
        saved_chunks = []
        for chunk_text in chunks:
            # 2. Generate embedding
            embedding = await embedding_service.generate_embedding(chunk_text)
            
            # 3. Store in DB
            db_chunk = TextChunk(
                content=chunk_text,
                embedding=embedding,
                metadata_=input.metadata,
                source="text_input"
            )
            db.add(db_chunk)
            saved_chunks.append(chunk_text)
            
        db.commit()
        
        return {
            "status": "success",
            "chunks_processed": len(saved_chunks),
            "message": "Text successfully ingested and indexed"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload file (PDF/Image), extract text, and index it.
    """
    try:
        # 1. Upload to Firebase Storage
        file_url = await storage_service.upload_file(file)
        
        # 2. Extract text based on file type
        text = ""
        if file.content_type == "application/pdf":
            text = await processing_service.extract_text_from_pdf(file)
        elif file.content_type in ["image/jpeg", "image/png"]:
            text = await processing_service.extract_text_from_image(file)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
            
        if not text:
            raise HTTPException(status_code=400, detail="Could not extract text from file")

        # 3. Chunk and Index (Reuse logic or call service)
        chunks = embedding_service.chunk_text(text)
        
        for chunk_text in chunks:
            embedding = await embedding_service.generate_embedding(chunk_text)
            
            db_chunk = TextChunk(
                content=chunk_text,
                embedding=embedding,
                metadata_={"original_filename": file.filename, "file_url": file_url},
                source=file.filename
            )
            db.add(db_chunk)
            
        db.commit()
        
        return {
            "status": "success",
            "file_url": file_url,
            "chunks_processed": len(chunks),
            "message": "File processed and indexed"
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
