from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials

from .core.config import get_settings
from .core.database import init_db

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Firebase
    if not firebase_admin._apps:
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
        firebase_admin.initialize_app(cred, {
            'storageBucket': settings.FIREBASE_STORAGE_BUCKET
        })
    
    # Initialize DB
    init_db()
    
    yield

from .routers import ingest, vector

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router)
app.include_router(vector.router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}
