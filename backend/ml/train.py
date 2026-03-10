import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Define path for saving the model
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(MODEL_DIR, 'model.pkl')

def generate_synthetic_data(samples=1000):
    """
    Generate synthetic sensor data to train the model.
    In a real scenario, this would come from historical database logs.
    """
    np.random.seed(42)
    
    # Generate random features
    temperature = np.random.uniform(15, 35, samples)
    humidity = np.random.uniform(30, 80, samples)
    motion = np.random.choice([0, 1], samples, p=[0.7, 0.3]) # 30% time motion detected
    
    # Light intensity (0-1000 lux)
    light_intensity = np.random.uniform(0, 1000, samples)
    
    # Target: Should the Living Room Light be ON (1) or OFF (0)?
    # Logic: If it is dark (light < 300) AND there is motion, turn light ON.
    # We add some noise to make it realistic
    target = []
    for l, m in zip(light_intensity, motion):
        if l < 400 and m == 1:
            target.append(1) # Turn ON
        else:
            # 5% chance user turns it on manually anyway
            target.append(np.random.choice([0, 1], p=[0.95, 0.05]))
            
    df = pd.DataFrame({
        'temperature': temperature,
        'humidity': humidity,
        'motion': motion,
        'light': light_intensity,
        'light_status': target
    })
    
    return df

def train_model():
    print("Generating synthetic dataset...")
    df = generate_synthetic_data(2000)
    
    X = df[['temperature', 'humidity', 'motion', 'light']]
    y = df['light_status']
    
    print("Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42)
    model.fit(X, y)
    
    # Evaluate simply (training accuracy)
    score = model.score(X, y)
    print(f"Model trained with training accuracy: {score:.2f}")
    
    # Save the model
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == '__main__':
    train_model()
