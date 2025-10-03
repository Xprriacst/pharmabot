from fastapi import APIRouter
from datetime import datetime
from app.config import settings

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }

@router.get("/status")
async def system_status():
    """Detailed system status"""
    return {
        "status": "operational",
        "services": {
            "api": "running",
            "rag": "ready",
            "database": "connected"
        },
        "timestamp": datetime.utcnow().isoformat()
    }
