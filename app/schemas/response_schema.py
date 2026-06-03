from enum import Enum
from typing import Optional

from pydantic import BaseModel

from app.schemas.metrics_schema import task_type as TaskType
from app.schemas.report_schema import evaluationSource


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