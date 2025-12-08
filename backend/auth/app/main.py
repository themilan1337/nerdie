"""
Auth Microservice - Main Application Entry Point.
FastAPI application with Firebase Auth integration.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .core.config import get_settings
from .core import firebase_client
from .routers import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    Initializes Firebase on startup.
    """
    # Startup
    firebase_client.initialize_firebase()
    print("✅ Firebase initialized successfully")
    yield
    # Shutdown
    print("👋 Auth service shutting down")


# Create FastAPI application
app = FastAPI(
    title="Nerdie Auth Service",
    description="Authentication microservice using Firebase Auth",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Get settings
settings = get_settings()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router.router)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with service information."""
    return {
        "service": "Nerdie Auth Service",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/auth/health"
    }

@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint."""
    return {"status": "ok"}
    
# Global exception handler for unhandled errors
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle unhandled exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred"
        }
    )
