"""
Ingestion API Router.

Provides endpoints for ingesting text, PDFs, and images.
All endpoints require Firebase Auth and include user_id isolation.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.auth import get_current_user
from ..services.embedding_service import embedding_service
from ..services.storage_service import storage_service
from ..services.processing_service import processing_service
from ..services.graph_service import graph_extraction_service
from ..services.firestore_service import firestore_service
from ..services.rag_client import rag_client


router = APIRouter(
    prefix="/ingest",
    tags=["Ingestion"]
)

security = HTTPBearer()


class TextInput(BaseModel):
    text: str
    metadata: Optional[dict] = {}


class FileUrlInput(BaseModel):
    file_url: str
    metadata: Optional[dict] = {}


@router.post("/text")
async def ingest_text(
    input: TextInput,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Ingest raw text, chunk it, generate embeddings, and store in vector DB.
    Extracts knowledge graph and stores in Firestore.
    """
    try:
        # Get user_id from Firebase token
        user_id = await get_current_user(credentials)
        
        # 1. Chunk text with overlap
        chunks = embedding_service.chunk_text(input.text)
        
        # 2. Process each chunk
        processed_chunks = []
        for chunk_text in chunks:
            # Generate embedding
            embedding = await embedding_service.generate_embedding(chunk_text)
            
            # Send to rag_service
            metadata = {
                **input.metadata,
                "type": "text",
                "source": "text_input"
            }
            
            result = await rag_client.insert_chunk(
                user_id=user_id,
                text=chunk_text,
                embedding=embedding,
                metadata=metadata
            )
            processed_chunks.append(result)
        
        # 3. Extract knowledge graph
        graph_data = await graph_extraction_service.extract_from_chunks(chunks)
        
        # 4. Save to Firestore
        if graph_data["entities"]:
            await firestore_service.save_entities(user_id, graph_data["entities"])
        if graph_data["relations"]:
            await firestore_service.save_relations(user_id, graph_data["relations"])
        
        return {
            "status": "success",
            "user_id": user_id,
            "chunks_processed": len(processed_chunks),
            "entities_extracted": len(graph_data["entities"]),
            "relations_extracted": len(graph_data["relations"]),
            "message": "Text successfully ingested and indexed"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pdf")
async def ingest_pdf(
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Upload PDF, extract text, chunk, embed, and index.
    """
    try:
        # Get user_id from Firebase token
        user_id = await get_current_user(credentials)
        
        # Validate file type
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="File must be a PDF")
        
        # 1. Upload to Firebase Storage
        file_url = await storage_service.upload_file(file, folder=f"pdfs/{user_id}")
        
        # 2. Extract text from PDF
        text = await processing_service.extract_text_from_pdf(file)
        
        if not text or len(text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        # 3. Chunk text
        chunks = embedding_service.chunk_text(text)
        
        # 4. Process each chunk
        processed_chunks = []
        for chunk_text in chunks:
            embedding = await embedding_service.generate_embedding(chunk_text)
            
            metadata = {
                "type": "pdf",
                "source": file.filename,
                "file_url": file_url
            }
            
            result = await rag_client.insert_chunk(
                user_id=user_id,
                text=chunk_text,
                embedding=embedding,
                metadata=metadata
            )
            processed_chunks.append(result)
        
        # 5. Extract knowledge graph
        graph_data = await graph_extraction_service.extract_from_chunks(chunks)
        
        # 6. Save to Firestore
        if graph_data["entities"]:
            await firestore_service.save_entities(user_id, graph_data["entities"])
        if graph_data["relations"]:
            await firestore_service.save_relations(user_id, graph_data["relations"])
        
        # 7. Save document metadata
        await firestore_service.save_document_metadata(
            user_id=user_id,
            filename=file.filename,
            file_url=file_url,
            file_type="pdf",
            chunks_count=len(chunks)
        )
        
        return {
            "status": "success",
            "user_id": user_id,
            "file_url": file_url,
            "chunks_processed": len(processed_chunks),
            "entities_extracted": len(graph_data["entities"]),
            "relations_extracted": len(graph_data["relations"]),
            "message": "PDF processed and indexed"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/image")
async def ingest_image(
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Upload image, OCR with Gemini Vision, chunk, embed, and index.
    """
    try:
        # Get user_id from Firebase token
        user_id = await get_current_user(credentials)
        
        # Validate file type
        if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
            raise HTTPException(status_code=400, detail="File must be JPEG, PNG, or WebP image")
        
        # 1. Upload to Firebase Storage
        file_url = await storage_service.upload_file(file, folder=f"images/{user_id}")
        
        # 2. Extract text using Gemini Vision OCR
        text = await processing_service.extract_text_from_image(file)
        
        if not text or len(text.strip()) < 5:
            # Still save image reference even without OCR text
            await firestore_service.save_document_metadata(
                user_id=user_id,
                filename=file.filename,
                file_url=file_url,
                file_type="image",
                chunks_count=0
            )
            return {
                "status": "success",
                "user_id": user_id,
                "file_url": file_url,
                "chunks_processed": 0,
                "message": "Image uploaded but no text could be extracted"
            }
        
        # 3. Chunk text
        chunks = embedding_service.chunk_text(text)
        
        # 4. Process each chunk
        processed_chunks = []
        for chunk_text in chunks:
            embedding = await embedding_service.generate_embedding(chunk_text)
            
            # Image chunks have special metadata for UI display
            metadata = {
                "type": "image",
                "source": file.filename,
                "file_url": file_url,
                "image_url": file_url  # For RAG response
            }
            
            result = await rag_client.insert_chunk(
                user_id=user_id,
                text=chunk_text,
                embedding=embedding,
                metadata=metadata
            )
            processed_chunks.append(result)
        
        # 5. Extract knowledge graph
        graph_data = await graph_extraction_service.extract_from_chunks(chunks)
        
        # 6. Save to Firestore
        if graph_data["entities"]:
            await firestore_service.save_entities(user_id, graph_data["entities"])
        if graph_data["relations"]:
            await firestore_service.save_relations(user_id, graph_data["relations"])
        
        # 7. Save document metadata
        await firestore_service.save_document_metadata(
            user_id=user_id,
            filename=file.filename,
            file_url=file_url,
            file_type="image",
            chunks_count=len(chunks)
        )
        
        return {
            "status": "success",
            "user_id": user_id,
            "file_url": file_url,
            "chunks_processed": len(processed_chunks),
            "entities_extracted": len(graph_data["entities"]),
            "relations_extracted": len(graph_data["relations"]),
            "message": "Image processed with OCR and indexed"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Keep legacy endpoint for backwards compatibility
@router.post("/upload")
async def upload_file_legacy(
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Legacy endpoint - routes to appropriate handler based on file type.
    """
    if file.content_type == "application/pdf":
        return await ingest_pdf(file, credentials, db)
    elif file.content_type in ["image/jpeg", "image/png", "image/webp"]:
        return await ingest_image(file, credentials, db)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Use PDF or image (JPEG/PNG/WebP)")
