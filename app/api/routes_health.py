"""Health check endpoints"""
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """API health check"""
    return {"status": "healthy"}


@router.get("/ready")
async def readiness_check():
    """Check if service is ready to accept requests"""
    # TODO: Check DB connection, etc.
    return {"status": "ready"}
