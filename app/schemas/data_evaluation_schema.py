from pydantic import BaseModel, Field

from app.schemas.metrics_schema import task_type as TaskType


class DataEvaluationMetadata(BaseModel):
    task_type: TaskType
    target_column: str = Field(..., example="Price")
    model_name: str = Field(..., example="Linear Regression")
    framework: str = Field(default="sklearn")