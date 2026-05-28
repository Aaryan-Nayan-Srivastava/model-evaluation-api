from fastapi import APIRouter
from app.utils.logger import get_logger
logger = get_logger(__name__)

router = APIRouter()

@router.get("/health")
async def health():
    logger.info("Health check endpoint called")
    return {
        "status": "ok",
        "message": "Model Evaluation API is healthy"
        }
