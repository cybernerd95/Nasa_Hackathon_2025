import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib  

# --- CONFIGURATION ---
TRAINING_DATA_FILE = r'D:\NASA_hackathon_2025\training_dataset_one_month.csv'
FEATURES = ['chlor_a', 'carbon_phyto', 'sst', 'ssha_karin']
TARGET = 'presence'
MODEL_FILE = r'D:\NASA_hackathon_2025\shark_rf_model.pkl'  # Path to save trained model

# --- 1. LOAD TRAINING DATA ---
df = pd.read_csv(TRAINING_DATA_FILE)

# Drop rows with missing values in features or target
df.dropna(subset=FEATURES + [TARGET], inplace=True)

X = df[FEATURES]
y = df[TARGET]

print(f"Training on {len(df)} samples with features: {FEATURES}")

# --- 2. TRAIN RANDOM FOREST MODEL ---
model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
model.fit(X, y)
print("Model training complete.")

# --- 3. SAVE MODEL ---
joblib.dump(model, MODEL_FILE)
print(f"Trained model saved to: {MODEL_FILE}")

# --- 4. HOW TO LOAD AND PREDICT ON NEW DATA ---
# Example usage:
new_data = pd.DataFrame({
    'chlor_a': [0.35, 0.3],
    'carbon_phyto': [33.7, 33],
    'sst': [21.0, 19.5],
    'ssha_karin': [10.30, 8.815]
})
loaded_model = joblib.load(MODEL_FILE)
predictions = loaded_model.predict(new_data)
probabilities = loaded_model.predict_proba(new_data)[:, 1]
print(probabilities)
