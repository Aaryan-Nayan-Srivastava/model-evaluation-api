import json
from typing import Any

from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel

from app.schemas.metrics_schema import task_type as TaskType


evaluation_prompt = PromptTemplate.from_template(
    """
You are an ML evaluation assistant.

Evaluate the following machine learning model using the provided structured evaluation data.

Model Name:
{model_name}

Task Type:
{task_type}

Processed Metrics:
{processed_metrics}

Experiment Metadata:
{experiment_metadata}

Return the evaluation using the required structured format.

Format Instructions:
{format_instructions}

Important rules:
- Do not assume metrics that are not present.
- Clearly mention missing important metrics.
- Base your judgment only on the provided metrics and metadata.
- Keep the explanation practical for ML deployment decisions.
- Recommendations must be specific and actionable.
""".strip()
)


def convert_to_serializable_dict(data: Any) -> dict[str, Any]:
    if data is None:
        return {}

    if isinstance(data, BaseModel):
        return data.model_dump(exclude_none=True)

    if isinstance(data, dict):
        return data

    return {"value": str(data)}


def build_evaluation_prompt(
    model_name: str,
    task_type: TaskType,
    processed_metrics: dict[str, Any],
    experiment_metadata: Any | None = None,
    format_instructions: str = ""
) -> str:


    metadata_dict = convert_to_serializable_dict(experiment_metadata)

    prompt = evaluation_prompt.format(
        model_name=model_name,
        task_type=task_type.value,
        processed_metrics=json.dumps(processed_metrics, indent=2),
        experiment_metadata=json.dumps(metadata_dict, indent=2),
        format_instructions=format_instructions,
    )

    return prompt