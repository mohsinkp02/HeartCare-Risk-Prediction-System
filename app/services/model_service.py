import joblib
import os
import logging
import numpy as np
from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class ModelService:
    _model = None

    @classmethod
    def load_model(cls):
        if cls._model is not None:
            return

        try:
            if os.path.exists(settings.MODEL_PATH):
                logger.info(f"Loading model from {settings.MODEL_PATH}...")
                cls._model = joblib.load(settings.MODEL_PATH)
                logger.info("Model loaded successfully!")
            else:
                logger.error(f"Model file {settings.MODEL_PATH} not found! Using Mock Model for demonstration.")
                cls._model = MockModel()
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            cls._model = MockModel()

    @classmethod
    def predict(cls, input_vector: list) -> dict:
        if cls._model is None:
            cls.load_model()
        
        input_array = [input_vector]
        
        # Predict
        try:
            prediction_prob = cls._model.predict_proba(input_array)[0][1]
            prediction_class = int(cls._model.predict(input_array)[0])
        except AttributeError:
             # Fallback for mock model or weird scikit versions
            prediction_prob = 0.5
            prediction_class = 0

        risk_level, risk_label = cls._calculate_risk_level(prediction_prob)

        return {
            "probability": float(prediction_prob),
            "class": prediction_class,
            "risk_level": risk_level,
            "risk_label": risk_label
        }

    @staticmethod
    def _calculate_risk_level(prob: float):
        if prob <= 0.20:
            return 1, "Very Low"
        elif prob <= 0.40:
            return 2, "Low"
        elif prob <= 0.60:
            return 3, "Moderate"
        elif prob <= 0.80:
            return 4, "High"
        else:
            return 5, "Very High"

class MockModel:
    """Mock model for when the real model is missing or fails to load."""
    def predict_proba(self, X):
        return np.array([[0.5, 0.5]]) # 50% chance
    
    def predict(self, X):
        return np.array([0])
