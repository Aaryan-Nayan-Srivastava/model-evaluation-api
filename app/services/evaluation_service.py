from app.schemas.request_schema import evaluationRequest
from app.schemas.response_schema import EvaluationResponse, ErrorResponse,ResponseStatus
from app.schemas.report_schema import evaluationSource
from app.schemas.metrics_schema import task_type
from app.services.metrics_service import preprocess_metrics
from uuid import uuid4

async def evaluate_from_metrics(request: evaluationRequest) ->EvaluationResponse:
    try:
        processed_metrics = preprocess_metrics(task_type=request.task_type,metrics=request.metrics)

        report_id = f"report_{uuid4().hex[:12]}"

        metric_count = len(processed_metrics["formatted_metrics"])
        missing_metrics = processed_metrics["missing_metrics"]
        metric_flags = processed_metrics["metric_flags"]

        if missing_metrics:
            missing_text = ", ".join(missing_metrics)
        else:
            missing_text = "None"

        flags_text = " ".join(metric_flags)

        return EvaluationResponse(
            message="Evaluation metrics processed successfully.",
            report_id=report_id,
            evaluation_source=evaluationSource.metrics,
            model_name=request.model_name,
            task_type=request.task_type,
            summary=(
                f"Processed {metric_count} metric(s) for {request.model_name}. "
                f"Missing optional metrics: {missing_text}. "
                f"Metric observations: {flags_text}"
            ),
            risk_level="Unknown",
            deployment_readiness="Not assessed yet",
        )
    except:
        return ErrorResponse(
            status=ResponseStatus.error,
            message="Evaluation failed",
            detail="An error occurred during evaluation. Please check the input data and try again."
        )


