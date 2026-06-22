from dataclasses import dataclass
from typing import Any

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
)

from app.schemas.metrics_schema import task_type as TaskType
# from app.services.dataset_service import DatasetSplit


@dataclass
class PredictionResult:
    prediction_count: int
    metrics: dict[str, float]


def generate_predictions(
    model: Any,
    features: pd.DataFrame,
) -> Any:
    """
    Generate predictions using the uploaded model.
    """

    if not hasattr(model, "predict"):
        raise ValueError("Model does not have a predict() method.")

    try:
        predictions = model.predict(features)

    except Exception as exc:
        raise ValueError(
            "Model prediction failed. Please check whether the dataset features match the model input."
        ) from exc

    return predictions


def calculate_classification_metrics(
    y_true: Any,
    y_pred: Any,
) -> dict[str, float]:
    """
    Calculate basic classification metrics.
    """

    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(
            precision_score(
                y_true,
                y_pred,
                average="weighted",
                zero_division=0,
            )
        ),
        "recall": float(
            recall_score(
                y_true,
                y_pred,
                average="weighted",
                zero_division=0,
            )
        ),
        "f1_score": float(
            f1_score(
                y_true,
                y_pred,
                average="weighted",
                zero_division=0,
            )
        ),
    }


def calculate_regression_metrics(
    y_true: Any,
    y_pred: Any,
) -> dict[str, float]:
    """
    Calculate basic regression metrics.
    """

    mse = float(mean_squared_error(y_true, y_pred))

    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "mse": mse,
        "rmse": mse ** 0.5,
        "r2_score": float(r2_score(y_true, y_pred)),
    }


def calculate_metrics(
    task_type: TaskType,
    y_true: Any,
    y_pred: Any,
) -> dict[str, float]:
    """
    Calculate metrics based on task type.
    """

    if task_type == TaskType.classification:
        return calculate_classification_metrics(
            y_true=y_true,
            y_pred=y_pred,
        )

    if task_type == TaskType.regression:
        return calculate_regression_metrics(
            y_true=y_true,
            y_pred=y_pred,
        )

    raise ValueError(f"Unsupported task type: {task_type}")


def run_prediction_and_metric_calculation(
    model: Any,
    x_Test: Any,
    y_Test: Any,
    task_type: TaskType,
) -> PredictionResult:
    """
    Main function used by /evaluate-from-data.

    It generates predictions and calculates evaluation metrics.
    """

    predictions = generate_predictions(
        model=model,
        features=x_Test,
    )

    metrics = calculate_metrics(
        task_type=task_type,
        y_true=y_Test,
        y_pred=predictions,
    )

    return PredictionResult(
        prediction_count=len(predictions),
        metrics=metrics,
    )