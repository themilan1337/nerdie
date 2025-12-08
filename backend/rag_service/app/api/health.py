"""
Health Check API Router.

Provides health check endpoint for Docker and orchestrators.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from ..core.db import get_db
from ..models.query import HealthResponse


router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check if the service and database are healthy"
)
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Health check endpoint.
    
    Verifies:
    - Service is running
    - Database connection is alive
    
    Used by Docker HEALTHCHECK and load balancers.
    """
    try:
        # Test database connection
        await db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    
    return HealthResponse(
        status="ok",
        service="rag_service",
        database=db_status
    )
