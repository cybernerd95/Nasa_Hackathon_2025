import tkinter as tk
from tkinter import messagebox
import joblib
import pandas as pd

# --- Load the trained model ---
model_path = r"D:\NASA_hackathon_2025\shark_rf_model.joblib"
model = joblib.load(model_path)

# --- GUI Setup ---
root = tk.Tk()
root.title("Shark Presence Predictor")

# Labels and entries for features
features = ['chlor_a', 'carbon_phyto', 'sst', 'ssha_karin']
entries = {}

for i, feature in enumerate(features):
    tk.Label(root, text=feature).grid(row=i, column=0, padx=10, pady=5, sticky='e')
    entry = tk.Entry(root)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries[feature] = entry

# Function to predict
def predict():
    try:
        # Read input values
        input_data = {f: [float(entries[f].get())] for f in features}
        df = pd.DataFrame(input_data)
        
        # Get prediction probability
        prob = model.predict_proba(df)[:, 1][0]
        pred = model.predict(df)[0]
        
        messagebox.showinfo("Prediction Result",
                            f"Predicted Presence: {pred}\nProbability of Presence: {prob:.3f}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values for all features.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Predict button
tk.Button(root, text="Predict", command=predict).grid(row=len(features), column=0, columnspan=2, pady=10)

# Run the GUI loop
root.mainloop()
