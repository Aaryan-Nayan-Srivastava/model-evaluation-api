from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_evaluate_with_valid_classification_payload():
    payload = {
        "task_type": "classification",
        "model_name": "RandomForestClassifier",
        "metrics": {
            "accuracy": 0.91,
            "precision": 0.88,
            "recall": 0.86,
            "f1_score": 0.87,
        },
        "experiment_metadata": {
            "dataset_name": "churn_data.csv",
            "dataset_size": 10000,
            "feature_count": 18,
            "target_column": "churn",
            "framework": "scikit-learn",
        },
    }

    response = client.post("/evaluate", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["evaluation_source"] == "metrics"
    assert data["model_name"] == "RandomForestClassifier"
    assert data["task_type"] == "classification"
    assert "report_id" in data
    assert data["message"] == "Evaluation metrics processed successfully."
    assert "Processed 4 metric" in data["summary"]
    assert "roc_auc" in data["summary"]
    assert "log_loss" in data["summary"]


def test_evaluate_with_valid_regression_payload():
    payload = {
        "task_type": "regression",
        "model_name": "LinearRegression",
        "metrics": {
            "mae": 12.5,
            "rmse": 18.2,
            "r2_score": 0.82,
        },
        "training_logs": [],
        "experiment_metadata": {
            "dataset_name": "house_prices.csv",
            "dataset_size": 5000,
            "feature_count": 12,
            "target_column": "price",
            "framework": "scikit-learn",
        },
    }

    response = client.post("/evaluate", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["evaluation_source"] == "metrics"
    assert data["model_name"] == "LinearRegression"
    assert data["task_type"] == "regression"
    assert "report_id" in data
    assert "Processed 3 metric" in data["summary"]
    assert "R2 score is strong" in data["summary"]