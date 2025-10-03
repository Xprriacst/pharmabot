from fastapi import APIRouter, BackgroundTasks
from datetime import datetime
from app.config import settings
import subprocess
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

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

@router.post("/load-demo-data")
async def load_demo_data(background_tasks: BackgroundTasks):
    """Load demonstration data into the database"""
    def load_data():
        try:
            logger.info("Starting demo data load...")
            subprocess.run(["python", "scripts/load_demo_data.py"], check=True, cwd=".")
            logger.info("Demo data loaded successfully")
        except Exception as e:
            logger.error(f"Error loading demo data: {e}")
    
    background_tasks.add_task(load_data)
    return {
        "status": "started",
        "message": "Demo data loading started in background"
    }
