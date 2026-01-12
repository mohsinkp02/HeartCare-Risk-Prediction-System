from fastapi import APIRouter, HTTPException, Depends
from app.schemas.prediction import PredictionInput, PredictionOutput
from app.services.preprocessing import PreprocessingService
from app.services.model_service import ModelService
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/predict", response_model=PredictionOutput)
async def predict(input_data: PredictionInput):
    """
    Predict heart disease risk based on patient data.
    """
    try:
        # 1. Convert Pydantic model to dict (using alias for keys to match model features)
        data_dict = input_data.model_dump(by_alias=True)
        
        # 2. Preprocess
        input_vector = PreprocessingService.process_input(data_dict)
        
        # 3. Predict
        result = ModelService.predict(input_vector)
        
        return result
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "heart-disease-prediction"}
