from pathlib import Path
import joblib
import pandas as pd

from ml.preprocessing.preprocessing import prepare_inference_data


BASE_DIR = Path(__file__).resolve().parent.parent

# --- CHANGED: load XGBoost model instead of Isolation Forest ---
MODEL_PATH           = BASE_DIR / "artifacts" / "xgboost_model.pkl"
LABEL_ENCODERS_PATH  = BASE_DIR / "artifacts" / "label_encoders.pkl"
FEATURE_COLUMNS_PATH = BASE_DIR / "artifacts" / "feature_columns.pkl"

# Load all artifacts once at startup (not on every request — better performance)
model           = joblib.load(MODEL_PATH)
label_encoders  = joblib.load(LABEL_ENCODERS_PATH)
feature_columns = joblib.load(FEATURE_COLUMNS_PATH)


def predict_transaction(transaction: dict):
    """
    Predict fraud for a single transaction.

    Returns a dictionary compatible with the existing API response schema:
        - prediction     : "Fraud" or "Normal"
        - action         : "Block" or "Approve"
        - risk_score     : 0–100 (higher = more risky)
        - confidence_score : 0–100 (how confident the model is)
        - model_version  : version string
    """

    # Convert the transaction dict to a single-row DataFrame
    df = pd.DataFrame([transaction])

    # Apply the same preprocessing used during training
    X = prepare_inference_data(df, label_encoders, feature_columns)

    # --- CHANGED: XGBoost uses predict_proba() for probability output ---
    # predict_proba() returns [P(Normal), P(Fraud)] for each row.
    # We take index [1] to get the fraud probability (0.0 to 1.0).
    fraud_probability = model.predict_proba(X)[0][1]

    # XGBoost's predict() returns 0 (Normal) or 1 (Fraud) directly.
    # No sign-flip conversion needed (unlike Isolation Forest's -1/+1 output).
    prediction_label = model.predict(X)[0]

    is_fraud = bool(prediction_label == 1)

    # Risk score: directly scaled from fraud probability (0–100)
    # A fraud probability of 0.95 → risk_score of 95
    risk_score = round(fraud_probability * 100, 2)

    # Confidence score: how far from 0.5 (the uncertain midpoint)
    # 0.5 = 50% confidence, 1.0 = 100% confidence
    confidence_score = round(abs(fraud_probability - 0.5) * 200, 2)

    return {
        "prediction":       "Fraud" if is_fraud else "Normal",
        "action":           "Block" if is_fraud else "Approve",
        "risk_score":       risk_score,
        "confidence_score": confidence_score,
        "model_version":    "v2.0.0",   # bumped to reflect XGBoost upgrade
    }