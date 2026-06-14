from enum import Enum
from typing import Optional

from pydantic import BaseModel,Field

from app.schemas.metrics_schema import task_type as TaskType
from app.schemas.report_schema import evaluationSource

class LLMEvaluationOutput(BaseModel):
    performance_summary: str = Field(
        ...,
        description="Clear summary of the model's performance based only on the provided metrics.",
    )
    risk_assessment: str = Field(
        ...,
        description="Risk assessment of the model for deployment.",
    )
    deployment_readiness: str = Field(
        ...,
        description="Deployment readiness decision or condition.",
    )
    recommendations: list[str] = Field(
        default_factory=list,
        description="Practical recommendations for improving or monitoring the model.",
    )
    risk_level: str = Field(
        default="Unknown",
        description="Overall risk level such as Low, Medium, High, or Critical.",
    )

class ResponseStatus(str, Enum):
    success = "success"
    error = "error"


class EvaluationResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.success
    message: str
    report_id: str
    evaluation_source: evaluationSource
    model_name: str
    task_type: TaskType
    summary: str
    risk_level: Optional[str] = None
    deployment_readiness: Optional[str] = None


class ErrorResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.error
    message: str
    detail: Optional[str] = None