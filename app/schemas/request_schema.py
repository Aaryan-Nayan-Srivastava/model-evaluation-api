from typing import Any, Optional
from pydantic import BaseModel, Field, model_validator
from app.schemas.metrics_schema import task_type, validate_metrics_by_task

class experimentMetadata(BaseModel):
    dataset_name: Optional[str] = None
    dataset_size: Optional[int] = Field(default=None, ge=1)
    feature_count: Optional[int] = Field(default=None, ge=1)
    target_column: Optional[str] = None
    framework: Optional[str] = None

class evaluationRequest(BaseModel):
    task_type: task_type
    model_name: str = Field(..., min_length=1)
    metrics: dict[str, Any]
    experiment_metadata: Optional[experimentMetadata] = None

    @model_validator(mode="after")
    def validate_metrics_match_task_type(self):
        validate_metrics_by_task(
            task_type=self.task_type,
            metrics=self.metrics,
        )
        return self


class dataEvaluationMetadata(BaseModel):
    model_name: str = Field(..., min_length=1)
    framework: str = Field(default="sklearn")
    dataset_name: Optional[str] = None
    target_column: Optional[str] = None