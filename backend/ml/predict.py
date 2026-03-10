import joblib
import os
import numpy as np

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(MODEL_DIR, 'model.pkl')

# Load model lazily
model = None

def load_model():
    global model
    if model is None:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
        else:
            print(f"Warning: Model not found at {MODEL_PATH}. AI features will not work until trained.")
            return False
    return True

def predict_device_state(temp, humidity, motion, light):
    """
    Predict if light should be ON or OFF.
    Returns: (decision (1/0), confidence_score)
    """
    if not load_model():
        return None, 0.0
        
    # Prepare features: temperature, humidity, motion, light
    # Assumes 'light' here is a numerical value like lux. 
    # If the simulator sends a string, it needs to be parsed in api.py, 
    # but for simplicity we assume we convert it to float if possible, 
    # or the simulator sends it as a float.
    
    try:
        light_val = float(light)
        temp_val = float(temp)
        hum_val = float(humidity)
        mot_val = int(motion) if type(motion) == bool else int(motion)
    except (ValueError, TypeError):
        # Handle case where sensor data isn't numerical
        return None, 0.0

    features = np.array([[temp_val, hum_val, mot_val, light_val]])
    
    # Predict probabilities
    probs = model.predict_proba(features)[0]
    decision = model.predict(features)[0]
    
    # Confidence is the probability of the chosen class
    confidence = probs[decision]
    
    return int(decision), float(confidence)
