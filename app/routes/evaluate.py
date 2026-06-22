import pandas as pd

from fastapi import APIRouter, HTTPException
from app.services.model_service import load_uploaded_model
from app.utils.logger import get_logger
from app.schemas.request_schema import evaluationRequest
from app.services.evaluation_service import evaluate_from_metrics
from fastapi import UploadFile, File, Form
from app.schemas.data_evaluation_schema import DataEvaluationMetadata
from app.schemas.response_schema import EvaluationResponse, evaluationSource
import json
from app.services.prediction_service import run_prediction_and_metric_calculation
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
    
@router.post("/evaluate-from-data")
async def evaluate_from_data(
    model_file: UploadFile = File(...),
    test_dataset_file: UploadFile = File(...),
    metadata: str = Form(...,json_schema_extra={
            "example": {
                "task_type": "regression",
                "target_column": "Price",
                "model_name": "Linear Regression"
            }})
):
    # metadata: str = Form(...)

    metadata_obj = DataEvaluationMetadata.model_validate_json(metadata)
    metadata_dict = metadata_obj.model_dump()

    try:
        model = await load_uploaded_model(model_file)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Model loading failed: {str(exc)}",
        )
    
    # x_test,y_Test generation
    target_column = metadata_dict["target_column"]
    data=pd.read_csv(test_dataset_file.file)
    if target_column not in data.columns:
        raise HTTPException(
            status_code=400,
            detail=f"Target column '{target_column}' not found in dataset."
        )
    y_test=data[target_column]
    x_test=data.drop(columns=[target_column])

    # prediction and metric calculation
    try:
        prediction_Result=run_prediction_and_metric_calculation(model,x_test,y_test,metadata_dict["task_type"])
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction and metric calculation failed: {str(exc)}",
        )
    metrics_text = ", ".join(
        f"{metric_name}: {metric_value:.4f}"
        for metric_name, metric_value in prediction_Result.metrics.items()
    )

    model_class_name = metadata_dict["model_name"]

    return EvaluationResponse(
        message="Predictions generated and metrics calculated successfully.",
        report_id="not_generated_yet",
        evaluation_source=evaluationSource.data,
        model_name=metadata_dict["model_name"],
        task_type=metadata_dict["task_type"],
        summary=(
            f"Generated {prediction_Result.prediction_count} prediction(s) using "
            f"model file '{model_file.filename}' and test dataset file '{test_dataset_file.filename}'. "
            f"Calculated metrics: {metrics_text}. "
            "LLM evaluation will be connected in the next phase."
        ),
        risk_level="Not assessed yet",
        deployment_readiness="Not assessed yet",
    )