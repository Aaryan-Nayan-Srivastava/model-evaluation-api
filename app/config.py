import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Model Evaluation Reporter")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    REPORT_JSON_DIR: str = os.getenv("REPORT_JSON_DIR", "reports/json")
    REPORT_MARKDOWN_DIR: str = os.getenv("REPORT_MARKDOWN_DIR", "reports/markdown")

    GROQ_MODEL_NAME: str = os.getenv("GROQ_MODEL_NAME", "llama-3.1-8b-instant")


settings = Settings()