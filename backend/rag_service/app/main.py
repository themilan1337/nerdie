"""
RAG Service - Main Application Entry Point.

FastAPI application for Retrieval-Augmented Generation with:
- PostgreSQL + pgvector for vector storage
- Gemini API for embeddings and generation
- Anti-hallucination prompts for grounded answers
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .core.config import get_settings
from .core.db import init_db, close_db
from .api import vector, rag, health, graph


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    
    Startup:
    - Initialize database and create tables
    - Create pgvector extension
    
    Shutdown:
    - Close database connections
    """
    # Startup
    await init_db()
    print("🚀 RAG Service started")
    yield
    # Shutdown
    await close_db()
    print("👋 RAG Service stopped")


# Get settings
settings = get_settings()

# Create FastAPI application
app = FastAPI(
    title="Nerdie RAG Service",
    description="""
    RAG (Retrieval-Augmented Generation) service for the Nerdie knowledge assistant.
    
    ## Features
    - Vector storage with pgvector
    - Semantic similarity search
    - Gemini-powered answer generation
    - Anti-hallucination safeguards
    
    ## Endpoints
    - **POST /vector/insert** - Insert document chunks
    - **POST /rag/query** - Query the knowledge base
    - **GET /health** - Health check
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(vector.router)
app.include_router(rag.router)
app.include_router(health.router)
app.include_router(graph.router)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with service information."""
    return {
        "service": "Nerdie RAG Service",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "vector_insert": "POST /vector/insert",
            "rag_query": "POST /rag/query",
            "graph_query": "GET /graph/query",
            "health": "GET /health"
        }
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle unhandled exceptions with consistent error format."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred"
        }
    )
