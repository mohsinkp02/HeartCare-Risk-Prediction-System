import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "Heart Disease Prediction API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Model Configuration
    MODEL_PATH: str = os.getenv("MODEL_PATH", "app/models/heart_disease_model.pkl")
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
