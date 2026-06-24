# ML Model Evaluation Assistant

A FastAPI-based application that evaluates Machine Learning models using either:

* User-provided metrics
* Uploaded model and test dataset files

The application uses Large Language Models (LLMs) to generate structured evaluation reports containing:

* Performance summaries
* Risk assessments
* Deployment readiness analysis
* Actionable recommendations

---

# Features

* Evaluate ML models using manually provided metrics
* Evaluate ML models using uploaded model and dataset files
* Automatic prediction generation
* Automatic metric calculation
* Classification and Regression support
* LLM-powered model assessment
* Structured output parsing
* Risk level analysis
* Deployment readiness evaluation
* Docker support
* Interactive Swagger API documentation

---

# Tech Stack

## Backend

* FastAPI
* Pydantic
* Uvicorn

## Machine Learning

* Scikit-Learn
* Joblib
* Pandas

## LLM Integration

* LangChain
* Groq
* Structured Output Parser

## Testing

* Pytest

## Deployment

* Docker

---

# Project Structure

```text
project-root/
│
├── app/
│   │
│   ├── routes/
│   │   ├── evaluation.py
│   │   └── evaluate_from_data.py
│   │
│   ├── services/
│   │   ├── evaluation_service.py
│   │   ├── metrics_service.py
│   │   ├── model_service.py
│   │   ├── prediction_service.py
│   │   ├── report_service.py
│   │   └── llm_service.py
│   │
│   ├── schemas/
│   │
│   ├── utils/
│   │
│   └── main.py
│
├── tests/
│
├── Dockerfile
├── requirements.txt
├── .env
└── README.md
```

---

# System Architecture

```text
                    ┌──────────────┐
                    │   FastAPI    │
                    └──────┬───────┘
                           │
          ┌────────────────┴────────────────┐
          │                                 │
          ▼                                 ▼

     POST /evaluate            POST /evaluate-from-data

          │                                 │
          ▼                                 ▼

  User Metrics Input             Model Upload
                                        │
                                        ▼
                                Dataset Upload
                                        │
                                        ▼
                                Prediction Service
                                        │
                                        ▼
                                Metric Calculation

          └────────────────┬────────────────┘
                           ▼

                  Evaluation Service

                           ▼

                    Metrics Processing

                           ▼

                     Prompt Builder

                           ▼

                        Groq LLM

                           ▼

                 Structured Output Parser

                           ▼

                    Report Generator

                           ▼

                  Evaluation Response
```

---

# Evaluation Workflows

## Workflow 1: Metrics-Based Evaluation

```text
User
 ↓
POST /evaluate
 ↓
Metrics Validation
 ↓
Metrics Processing
 ↓
Prompt Generation
 ↓
Groq LLM
 ↓
Structured Output Parsing
 ↓
Evaluation Report
 ↓
Response
```

---

## Workflow 2: Data-Based Evaluation

```text
User
 ↓
POST /evaluate-from-data
 ↓
Upload Model
 ↓
Upload Test Dataset
 ↓
Generate Predictions
 ↓
Calculate Metrics
 ↓
Create Internal Evaluation Request
 ↓
Evaluation Service
 ↓
Groq LLM
 ↓
Structured Output Parsing
 ↓
Evaluation Report
 ↓
Response
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>

cd <repository-name>
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / Mac

```bash
python -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
```

---

# Running Locally

```bash
uvicorn app.main:app --reload
```

Application:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

---

# Docker Setup

## Build Image

```bash
docker build -t ml-evaluator .
```

---

## Run Container

```bash
docker run \
--env-file .env \
-p 8000:8000 \
ml-evaluator
```

---

## Access Application

```text
http://localhost:8000/docs
```

---

# API Endpoints

## 1. Evaluate Using Metrics

### Endpoint

```http
POST /evaluate
```

### Example Request

```json
{
  "task_type": "classification",
  "model_name": "RandomForestClassifier",
  "metrics": {
    "accuracy": 0.91,
    "precision": 0.89,
    "recall": 0.88,
    "f1_score": 0.90
  },
  "experiment_metadata": {
    "framework": "scikit-learn"
  }
}
```

### Example Response

```json
{
  "status": "success",
  "message": "Evaluation report generated successfully.",
  "report_id": "report_xxxxx",
  "evaluation_source": "metrics",
  "model_name": "RandomForestClassifier",
  "task_type": "classification",
  "summary": "...",
  "risk_level": "Low",
  "deployment_readiness": "Ready"
}
```

---

## 2. Evaluate Using Uploaded Files

### Endpoint

```http
POST /evaluate-from-data
```

### Inputs

#### model_file

```text
.pkl
.joblib
```

#### test_dataset_file

```text
.csv
```

#### metadata

```json
{
  "task_type": "regression",
  "target_column": "Price",
  "model_name": "Linear Regression"
}
```

### Processing Steps

```text
Load Model
 ↓
Load Dataset
 ↓
Generate Predictions
 ↓
Calculate Metrics
 ↓
Create Internal Evaluation Request
 ↓
LLM Evaluation
 ↓
Return Response
```

---

# Supported Tasks

## Classification

Supported metrics:

```text
Accuracy
Precision
Recall
F1 Score
```

---

## Regression

Supported metrics:

```text
MAE
MSE
RMSE
R² Score
```

---

# Example Use Cases

* Model performance review
* Pre-deployment validation
* Experiment comparison
* ML project demonstrations
* Educational ML projects
* Portfolio projects
* Automated model assessment

---

# Future Improvements

* Authentication and authorization
* Multi-model comparison
* Model explainability integration
* Batch evaluation support
* Cloud deployment
* CI/CD pipeline integration
* Evaluation history tracking

---

# Learning Outcomes

This project demonstrates:

* FastAPI development
* REST API design
* Pydantic validation
* LangChain integration
* Groq LLM integration
* Structured output parsing
* Machine Learning model evaluation
* Dockerization
* Automated testing
* Clean project architecture

---

# Author

Built as a Machine Learning + Generative AI project for automated model evaluation and reporting.
