from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)

# Feature Configuration (18 Features) - EXACT ORDER
MODEL_FEATURES = [
    'General_Health', 'Checkup', 'Exercise', 'Skin_Cancer', 'Other_Cancer', 
    'Depression', 'Diabetes', 'Arthritis', 'Sex', 'Age', 'Height', 'Weight', 
    'BMI', 'Smoking', 'Alcohol', 'Fruit', 'Green_Vegetables', 'Fried_Potato'
]

SCALERS = {
    'Weight': {'min': 29.94, 'max': 136.0},
    'Height': {'min': 142.0, 'max': 200.0},
    'BMI': {'min': 12.87, 'max': 43.28},
    'Age': {'min': 21, 'max': 82},
    'Fruit': {'min': 0, 'max': 56.0},
    'Green_Vegetables': {'min': 0, 'max': 44.0},
    'Fried_Potato': {'min': 0, 'max': 17.0},
    'Alcohol': {'min': 0, 'max': 15.0},
    'General_Health': {
        'Excellent': 1.0, 'Very_Good': 0.75, 'Good': 0.5, 'Fair': 0.25, 'Poor': 0.0
    },
    'Checkup': {
        'Within 1 year': 1.0, '1-2 years': 0.75, '2-5 years': 0.5, '5+ years': 0.25, 'Never': 0.0
    },
    'Diabetes': {
        'No': 0.0, 'Borderline': 0.33, 'During Pregnancy': 0.66, 'Yes': 1.0
    },
    'Sex': {'Female': 0.0, 'Male': 1.0, '0': 0.0, '1': 1.0},
    'Exercise': {'0': 0.0, '1': 1.0},
    'Smoking': {'0': 0.0, '1': 1.0},
    'Skin_Cancer': {'0': 0.0, '1': 1.0},
    'Other_Cancer': {'0': 0.0, '1': 1.0},
    'Depression': {'0': 0.0, '1': 1.0},
    'Arthritis': {'0': 0.0, '1': 1.0}
}

class PreprocessingService:
    @staticmethod
    def process_input(data: Dict[str, Any]) -> List[float]:
        input_vector = []
        for feature in MODEL_FEATURES:
            raw_val = data.get(feature)
            processed_val = PreprocessingService._process_single_value(raw_val, feature)
            input_vector.append(processed_val)
        return input_vector

    @staticmethod
    def _process_single_value(value: Any, feature_name: str) -> float:
        val_str = str(value).lower()
        
        if feature_name in SCALERS:
            config = SCALERS[feature_name]
            
            # Numeric Range Scaling
            if isinstance(config, dict) and 'min' in config:
                try:
                    val = float(value)
                    norm_val = (val - config['min']) / (config['max'] - config['min'])
                    return max(0.0, min(1.0, norm_val))
                except (ValueError, TypeError):
                    logger.warning(f"Failed to convert numeric value '{value}' for feature '{feature_name}'. Defaulting to 0.0.")
                    return 0.0
            
            # Categorical Logic
            elif isinstance(config, dict):
                # Exact match
                if str(value) in config:
                    return config[str(value)]
                
                # Check normalized key (e.g. for "Very_Good" vs "Very Good" if needed, though Pydantic handles validation)
                # But let's keep the logic from original app just in case
                if val_str in ['on', 'true', 'yes']: return 1.0
                if val_str in ['off', 'false', 'no']: return 0.0
                
                logger.warning(f"Unknown categorical value '{value}' for feature '{feature_name}'. Defaulting to 0.0.")
                return 0.0
        
        # Default fallback
        try:
            return float(value)
        except:
            return 0.0
