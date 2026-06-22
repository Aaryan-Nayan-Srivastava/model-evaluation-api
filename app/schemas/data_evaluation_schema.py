from pydantic import BaseModel

from app.schemas.metrics_schema import task_type as TaskType


class DataEvaluationMetadata(BaseModel):
    task_type: TaskType
    target_column: str
    model_name: str