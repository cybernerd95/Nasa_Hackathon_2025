import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from joblib import load

# --- 1. CONFIGURATION ---

# Path to your trained Random Forest model
MODEL_FILE = r"D:\NASA_hackathon_2025\shark_rf_model.joblib"

# Path to your input CSV file with environmental features for prediction
INPUT_CSV = r"D:\NASA_hackathon_2025\prediction_input.csv"

# Path to save predictions
OUTPUT_CSV = r"D:\NASA_hackathon_2025\prediction_output.csv"

# Columns expected by the model (must match training)
FEATURES = ['chlor_a', 'carbon_phyto', 'sst', 'ssha_karin']

# Probability threshold for predicting presence
THRESHOLD = 0.5  # default 0.3; lower to catch borderline cases

# --- 2. SCRIPT ---

# Load the trained Random Forest model
model = load(MODEL_FILE)

# Load input data
df = pd.read_csv(INPUT_CSV)

# Ensure the input has all required features
missing_cols = [col for col in FEATURES if col not in df.columns]
if missing_cols:
    raise ValueError(f"Input CSV is missing required features: {missing_cols}")

X = df[FEATURES]

# Predict probabilities
probs = model.predict_proba(X)[:, 1]  # probability of presence=1

# Apply threshold to get predicted presence
predicted_presence = (probs >= THRESHOLD).astype(int)

# Add predictions to dataframe
df['predicted_prob'] = probs
df['predicted_presence'] = predicted_presence

# Save to CSV
df.to_csv(OUTPUT_CSV, index=False)

print(f"Prediction complete! Results saved to '{OUTPUT_CSV}'")
print(df.head())
