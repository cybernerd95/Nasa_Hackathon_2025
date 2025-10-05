import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt
import joblib
import pickle

# --- CONFIGURATION ---
TRAINING_DATA_FILE = r"D:\NASA_hackathon_2025\training_dataset_one_month.csv"

FEATURES = ["chlor_a", "carbon_phyto", "sst", "ssha_karin"]
TARGET = "presence"
N_FOLDS = 5   # Stratified folds (guarantees both classes in each)

# --- SCRIPT ---
def train_and_evaluate_model():
    print(f"--- Loading training data from '{TRAINING_DATA_FILE}' ---")
    df = pd.read_csv(TRAINING_DATA_FILE)

    # Drop rows with missing values in relevant columns
    columns_to_check = FEATURES + [TARGET]
    initial_rows = len(df)
    df.dropna(subset=columns_to_check, inplace=True)
    print(f"Dropped {initial_rows - len(df)} rows with missing data.")

    if df.empty:
        print("No data left after cleaning. Exiting.")
        return

    X = df[FEATURES]
    y = df[TARGET]

    # Step 1: Show overall class balance
    print("\n--- Overall class distribution ---")
    print(y.value_counts())

    # Step 2: StratifiedKFold setup
    print(f"\n--- Performing {N_FOLDS}-fold Stratified Cross-Validation ---")
    skf = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=42)

    auc_scores = []
    feature_importances = pd.DataFrame(0, index=X.columns, columns=["importance"])

    for fold, (train_idx, test_idx) in enumerate(skf.split(X, y)):
        print(f"\nFold {fold+1}/{N_FOLDS}")
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        print(" Train class balance:")
        print(y_train.value_counts())
        print(" Test class balance:")
        print(y_test.value_counts())

        # Train Random Forest
        model = RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            n_jobs=-1,
            class_weight="balanced"
        )
        model.fit(X_train, y_train)

        # Predict probabilities
        y_pred_proba = model.predict_proba(X_test)[:, 1]

        # Compute AUC
        auc = roc_auc_score(y_test, y_pred_proba)
        auc_scores.append(auc)
        print(f"  AUC for this fold: {auc:.4f}")

        # Add feature importances
        feature_importances["importance"] += model.feature_importances_

    # Step 3: Final results
    print("\n\n--- FINAL RESULTS ---")
    mean_auc = np.mean(auc_scores)
    std_auc = np.std(auc_scores)
    print(f"Average Model Performance (AUC):")
    print(f"  Mean AUC: {mean_auc:.4f}")
    print(f"  Std Dev : {std_auc:.4f}")
    print("(AUC of 0.5 = random, 1.0 = perfect. >0.7 is good)")

    # Normalize importances
    feature_importances["importance"] /= N_FOLDS
    feature_importances.sort_values(by="importance", ascending=False, inplace=True)
    print("\nMost Important Environmental Variables:")
    print(feature_importances)

    # Plot feature importances
    feature_importances.plot(kind="barh", legend=False)
    plt.title("Feature Importance for Shark Habitat Model")
    plt.xlabel("Importance")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig("feature_importance_stratified.png")
    print("\nSaved feature importance plot to 'feature_importance_stratified.png'")

    # Step 4: Train final model on ALL data
    print("\n--- Training final model on ALL data ---")
    final_model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced"
    )
    final_model.fit(X, y)

    # Save the model (joblib and pickle)
    joblib.dump(final_model, "shark_rf_model.joblib")
    with open("shark_rf_model.pkl", "wb") as f:
        pickle.dump(final_model, f)

    print("Saved final model as 'shark_rf_model.joblib' and 'shark_rf_model.pkl'")

# --- RUN ---
if __name__ == "__main__":
    train_and_evaluate_model()
