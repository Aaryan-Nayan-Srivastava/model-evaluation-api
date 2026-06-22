from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from app.config import settings
from app.utils.logger import get_logger

from app.routes import health
from app.routes import evaluate

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Model Evaluation Reporter API")
    Path(settings.REPORT_JSON_DIR).mkdir(parents=True, exist_ok=True)
    Path(settings.REPORT_MARKDOWN_DIR).mkdir(parents=True, exist_ok=True)
    yield
    logger.info("Shutting down Model Evaluation Reporter API")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

app.include_router(health.router)
app.include_router(evaluate.router)
# app.include_router(evaluate_from_data.router)

@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {
        "message": "Welcome to Model Evaluation Reporter API",
        "docs": "/docs",
        "health": "/health",
        "evaluate": "/evaluate",
        "evaluate_from_data": "/evaluate-from-data"
    }