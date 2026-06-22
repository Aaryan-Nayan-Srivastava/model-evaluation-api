from app.schemas.request_schema import evaluationRequest
from app.schemas.response_schema import EvaluationResponse, ErrorResponse, ResponseStatus
from app.schemas.report_schema import evaluationSource
from app.services.llm_service import (
    generate_structured_llm_evaluation,
    get_format_instructions,
)
from app.services.metrics_service import preprocess_metrics
from app.services.report_service import generate_evaluation_report
from app.utils.prompts import build_evaluation_prompt
from app.utils.logger import get_logger
from app.schemas.report_schema import evaluationReport
logger = get_logger(__name__)



async def evaluate_from_metrics(request: evaluationRequest, evaluation_source: evaluationSource=evaluationSource.metrics) -> EvaluationResponse:

    try:
        processed_metrics = preprocess_metrics(
            task_type=request.task_type,
            metrics=request.metrics,
        )

        format_instructions = get_format_instructions()

        prompt = build_evaluation_prompt(
            model_name=request.model_name,
            task_type=request.task_type,
            processed_metrics=processed_metrics,
            experiment_metadata=request.experiment_metadata,
            format_instructions=format_instructions,
        )

        llm_output = await generate_structured_llm_evaluation(prompt)

        report = generate_evaluation_report(
            request=request,
            processed_metrics=processed_metrics,
            llm_output=llm_output,
            evaluation_source=evaluation_source,
        )

        recommendations_text = " ".join(
            f"{index + 1}. {recommendation}"
            for index, recommendation in enumerate(report.content.recommendations)
        )

        summary = f"""
            Performance Summary:
            {report.content.performance_summary}

            Risk Assessment:
            {report.content.risk_assessment}

            Recommendations:
            {recommendations_text}
        """.strip()
        return EvaluationResponse(
            message="Evaluation report generated successfully.",
            report_id=report.metadata.report_id,
            evaluation_source=report.metadata.evaluation_source,
            model_name=report.metadata.model_name,
            task_type=report.metadata.task_type,
            summary=summary,
            risk_level=llm_output.risk_level,
            deployment_readiness=report.content.deployment_readiness,
        )
    except Exception as e:
        logger.exception("Error occurred during evaluation")

        return ErrorResponse(
            status=ResponseStatus.error,
            message="Evaluation failed",
            detail=str(e),
        )


