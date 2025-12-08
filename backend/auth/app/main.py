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
    title="🔐 Nerdie Auth Service",
    description="""
    ## Google Firebase Authentication Service

    Микросервис авторизации для Nerdie, работающий **только через Google OAuth** с использованием Firebase.

    ### 🚀 Основные возможности:
    - ✅ Авторизация через Google OAuth (Firebase)
    - ✅ JWT токены с автоматическим обновлением
    - ✅ Защищённые endpoints с Bearer токеном
    - ✅ Получение информации о пользователе
    - ✅ CORS настроен для фронтенда

    ### 📚 Документация:
    - [Swagger UI](/docs) - интерактивная документация API
    - [ReDoc](/redoc) - альтернативная документация
    - Примеры запросов в файле `API_EXAMPLES.md`

    ### 🔗 Endpoints:
    - `POST /auth/google` - Авторизация через Google
    - `GET /auth/me` - Получить текущего пользователя
    - `GET /auth/health` - Health check

    ### ⚠️ Важно:
    Email/password авторизация **удалена**. Только Google OAuth!
    """,
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    contact={
        "name": "Nerdie Team",
        "url": "https://github.com/your-org/nerdie",
    },
    license_info={
        "name": "MIT",
    }
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
