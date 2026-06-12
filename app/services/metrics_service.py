from typing import Any
from app.schemas.metrics_schema import  task_type as TaskType


CLASSIFICATION_EXPECTED_METRICS = [
    "accuracy",
    "precision",
    "recall",
    "f1_score",
    "roc_auc",
    "log_loss",
]
REGRESSION_EXPECTED_METRICS = [
    "mae",
    "mse",
    "rmse",
    "r2_score"
]


def format_metrics(metrics: dict[str, Any]) -> dict[str, str]:

    formatted_metrics = {}

    for metric_name, metric_value in metrics.items():
        if metric_value is None:
            continue
        if isinstance(metric_value, (int, float)):
            formatted_metrics[metric_name] = f"{metric_value:.4f}"
        else:
            formatted_metrics[metric_name] = str(metric_value)
    return formatted_metrics


def detect_missing_metrics(task_type: TaskType,metrics: dict[str, Any]) -> list[str]:

    if task_type == TaskType.classification:
        expected_metrics = CLASSIFICATION_EXPECTED_METRICS
    else:
        expected_metrics = REGRESSION_EXPECTED_METRICS

    missing_metrics = []

    for metric_name in expected_metrics:
        if metric_name not in metrics or metrics.get(metric_name) is None:
            missing_metrics.append(metric_name)
    return missing_metrics


def generate_classification_flags(metrics: dict[str, Any]) -> list[str]:

    flags = []

    accuracy = metrics.get("accuracy")
    precision = metrics.get("precision")
    recall = metrics.get("recall")
    f1_score = metrics.get("f1_score")
    roc_auc = metrics.get("roc_auc")

    if accuracy is not None:
        if accuracy >= 0.85:
            flags.append("Accuracy is strong.")
        elif accuracy >= 0.70:
            flags.append("Accuracy is acceptable but can be improved.")
        else:
            flags.append("Accuracy is low and needs improvement.")

    if precision is not None:
        if precision >= 0.85:
            flags.append("Precision is strong.")
        elif precision < 0.60:
            flags.append("Precision is weak, which may indicate many false positives.")

    if recall is not None:
        if recall >= 0.85:
            flags.append("Recall is strong.")
        elif recall < 0.60:
            flags.append("Recall is weak, which may indicate many false negatives.")

    if f1_score is not None:
        if f1_score >= 0.80:
            flags.append("F1 score is strong and indicates balanced performance.")
        elif f1_score < 0.60:
            flags.append("F1 score is low and indicates weak balance between precision and recall.")

    if roc_auc is not None:
        if roc_auc >= 0.85:
            flags.append("ROC AUC is strong.")
        elif roc_auc < 0.70:
            flags.append("ROC AUC is low, so ranking quality may be weak.")

    if not flags:
        flags.append("Metrics were received, but no strong conclusion can be made yet.")

    return flags


def generate_regression_flags(metrics: dict[str, Any]) -> list[str]:

    flags = []

    r2_score = metrics.get("r2_score")
    mae = metrics.get("mae")
    rmse = metrics.get("rmse")
    mse = metrics.get("mse")

    if r2_score is not None:
        if r2_score >= 0.80:
            flags.append("R2 score is strong and indicates good model fit.")
        elif r2_score >= 0.50:
            flags.append("R2 score is moderate.")
        elif r2_score >= 0:
            flags.append("R2 score is weak and the model may not explain the target well.")
        else:
            flags.append("R2 score is negative, meaning the model performs worse than a simple baseline.")

    if mae is not None:
        flags.append(f"MAE is {mae}, which should be interpreted based on the target scale.")

    if mse is not None:
        flags.append(f"MSE is {mse}, which should be interpreted based on the target scale.")

    if rmse is not None:
        flags.append(f"RMSE is {rmse}, which highlights larger prediction errors.")

    if not flags:
        flags.append("Metrics were received, but no strong conclusion can be made yet.")

    return flags


def generate_metric_flags(task_type: TaskType,metrics: dict[str, Any]) -> list[str]:

    if task_type == TaskType.classification:
        return generate_classification_flags(metrics)

    return generate_regression_flags(metrics)


def preprocess_metrics(task_type: TaskType,metrics: dict[str, Any]) -> dict[str, Any]:

    formatted_metrics = format_metrics(metrics)
    missing_metrics = detect_missing_metrics(task_type, metrics)
    metric_flags = generate_metric_flags(task_type, metrics)

    return {
        "formatted_metrics": formatted_metrics,
        "missing_metrics": missing_metrics,
        "metric_flags": metric_flags,
    }