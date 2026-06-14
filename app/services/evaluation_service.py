from app.schemas.request_schema import evaluationRequest
from app.schemas.response_schema import EvaluationResponse, ErrorResponse,ResponseStatus
from app.schemas.report_schema import evaluationSource
from app.schemas.metrics_schema import task_type
from app.utils.prompts import build_evaluation_prompt
from app.services.metrics_service import preprocess_metrics
from app.services.llm_service import generate_structured_llm_evaluation
from uuid import uuid4
from app.utils.logger import get_logger
from app.services.llm_service import get_format_instructions
logger = get_logger(__name__)

async def evaluate_from_metrics(request: evaluationRequest) ->EvaluationResponse:
    try:
        processed_metrics = preprocess_metrics(task_type=request.task_type,metrics=request.metrics)

        logger.info(f"Processed metrics for model {request.model_name} and task type {request.task_type}")

        format_instructions = get_format_instructions()

        prompt = build_evaluation_prompt(request.model_name,
                                         request.task_type,
                                        processed_metrics,
                                        request.experiment_metadata
                                        ,format_instructions=format_instructions)
        logger.info(f"Built evaluation prompt for model {request.model_name} and task type {request.task_type}")

        report_content = await generate_structured_llm_evaluation(prompt)
        logger.info(f"Generated LLM evaluation report for model {request.model_name} and task type {request.task_type}")

        report_id = f"report_{uuid4().hex[:12]}"

        recommendations_text="\n".join(f"{index+1}. {recommendation}" for index, recommendation in enumerate(report_content.recommendations))

        summary = (
        f"{report_content.performance_summary} "
        f"Risk Assessment: {report_content.risk_assessment} "
        f"Recommendations: {recommendations_text}"
        )
        
        return EvaluationResponse(
            message="Evaluation metrics processed successfully.",
            report_id=report_id,
            evaluation_source=evaluationSource.metrics,
            model_name=request.model_name,
            task_type=request.task_type,
            summary=summary,
            risk_level=report_content.risk_level,
            deployment_readiness=report_content.deployment_readiness,
        )
    except:
        return ErrorResponse(
            status=ResponseStatus.error,
            message="Evaluation failed",
            detail="An error occurred during evaluation. Please check the input data and try again."
        )


