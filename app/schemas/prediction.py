from pydantic import BaseModel, Field
from typing import Literal

class PredictionInput(BaseModel):
    general_health: Literal['Excellent', 'Very_Good', 'Good', 'Fair', 'Poor'] = Field(..., alias="General_Health")
    checkup: Literal['Within 1 year', '1-2 years', '2-5 years', '5+ years', 'Never'] = Field(..., alias="Checkup")
    exercise: Literal['0', '1'] = Field(..., alias="Exercise")
    skin_cancer: Literal['0', '1'] = Field(..., alias="Skin_Cancer")
    other_cancer: Literal['0', '1'] = Field(..., alias="Other_Cancer")
    depression: Literal['0', '1'] = Field(..., alias="Depression")
    diabetes: Literal['No', 'Borderline', 'During Pregnancy', 'Yes'] = Field(..., alias="Diabetes")
    arthritis: Literal['0', '1'] = Field(..., alias="Arthritis")
    sex: Literal['0', '1'] = Field(..., alias="Sex")
    age: float = Field(..., ge=18, le=100, alias="Age")
    height: float = Field(..., ge=50, le=300, alias="Height")
    weight: float = Field(..., ge=10, le=500, alias="Weight")
    bmi: float = Field(..., ge=5, le=100, alias="BMI")
    smoking: Literal['0', '1'] = Field(..., alias="Smoking")
    alcohol: float = Field(..., ge=0, le=30, alias="Alcohol") # Assuming days/month? Logic in original app was weird (0-30)
    fruit: float = Field(..., ge=0, le=100, alias="Fruit")
    green_vegetables: float = Field(..., ge=0, le=100, alias="Green_Vegetables")
    fried_potato: float = Field(..., ge=0, le=100, alias="Fried_Potato")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "General_Health": "Good",
                "Checkup": "Within 1 year",
                "Exercise": "1",
                "Skin_Cancer": "0",
                "Other_Cancer": "0",
                "Depression": "0",
                "Diabetes": "No",
                "Arthritis": "0",
                "Sex": "0",
                "Age": 30,
                "Height": 175,
                "Weight": 70,
                "BMI": 22.5,
                "Smoking": "0",
                "Alcohol": 0,
                "Fruit": 10,
                "Green_Vegetables": 10,
                "Fried_Potato": 0
            }
        }

class PredictionOutput(BaseModel):
    probability: float
    class_label: int = Field(..., alias="class")
    risk_level: int
    risk_label: str

    class Config:
        populate_by_name = True
