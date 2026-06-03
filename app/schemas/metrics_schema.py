from enum import enum
from pydantic import BaseModel, Field, model_validator
from typing import Optional



class task_type(str,enum):
    classification = "classification"
    regression = "regression"

class classificationMetrics(BaseModel):
    accuracy: Optional[float]=Field(None,ge=0,le=1, description="The accuracy of the classification model.")
    precision: Optional[float]=Field(None,ge=0,le=1, description="The precision of the classification model.")
    recall: Optional[float]=Field(None,ge=0,le=1, description="The recall of the classification model.")
    f1_score: Optional[float]=Field(None,ge=0,le=1, description="The F1 score of the classification model.")
    roc_auc: Optional[float]=Field(None,ge=0,le=1, description="The ROC AUC score of the classification model.")
    log_loss: Optional[float]=Field(None,ge=0,le=1, description="The log loss of the classification model.")

    @model_validator(mode="after")
    def validate_at_least_one_metric(self):
        metric_values = self.model_dump(exclude_none=True)

        if not metric_values:
            raise ValueError("At least one classification metric must be provided.")

        return self
    
class regressionMetrics(BaseModel):
    mse: Optional[float]=Field(None,ge=0, description="The mean squared error of the regression model.")
    mae: Optional[float]=Field(None,ge=0, description="The mean absolute error of the regression model.")
    rmse: Optional[float]=Field(None,ge=0, description="The root mean squared error of the regression model.")
    r2_score: Optional[float]=Field(None, description="The R^2 score of the regression model.")

    @model_validator(mode="after")
    def validate_at_least_one_metric(self):
        metric_values = self.model_dump(exclude_none=True)

        if not metric_values:
            raise ValueError("At least one regression metric must be provided.")

        return self

def validate_metrics_by_task(task_type : task_type,metrics:dict):
    if task_type==task_type.classification:
        return classificationMetrics.model_validate(metrics)
    elif task_type==task_type.regression:
        return regressionMetrics.model_validate(metrics)
    else:
        raise ValueError("Invalid task type. Must be 'classification' or 'regression'.")
    