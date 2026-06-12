from fastapi import APIRouter, HTTPException
from app.utils.logger import get_logger
from app.schemas.request_schema import evaluationRequest
from app.services.evaluation_service import evaluate_from_metrics
logger = get_logger(__name__)


router=APIRouter()

@router.post("/evaluate")
async def evaluate_model(request:evaluationRequest):
    logger.info(f"Received evaluation request for model: {request.model_name} with task type: {request.task_type}")
    try:
        evaluation_response = await evaluate_from_metrics(request)
        logger.info(f"Evaluation completed successfully for model: {request.model_name}")
        return evaluation_response
    except Exception as e:
        logger.error(f"Error during evaluation for model: {request.model_name} - {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred during evaluation. Please check the input data and try again.")