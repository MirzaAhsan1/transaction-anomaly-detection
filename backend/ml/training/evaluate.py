from pathlib import Path
import joblib
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix

# Preprocessing pipeline is unchanged — reused as-is
from ml.preprocessing.preprocessing import prepare_inference_data


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET = BASE_DIR / "datasets" / "generated_transactions.csv"

# --- CHANGED: point to the new XGBoost model file ---
MODEL_PATH          = BASE_DIR / "artifacts" / "xgboost_model.pkl"
LABEL_ENCODERS_PATH = BASE_DIR / "artifacts" / "label_encoders.pkl"
FEATURE_COLUMNS_PATH = BASE_DIR / "artifacts" / "feature_columns.pkl"

print("Loading dataset...")
df = pd.read_csv(DATASET)

if "label" in df.columns:
    y = df["label"]
else:
    y = None
    print("Warning: 'label' column not found in dataset. Evaluation might not be possible.")

print("Loading artifacts...")
model           = joblib.load(MODEL_PATH)
label_encoders  = joblib.load(LABEL_ENCODERS_PATH)
feature_columns = joblib.load(FEATURE_COLUMNS_PATH)

print("Preparing inference data...")
X = prepare_inference_data(df, label_encoders, feature_columns)

print("Predicting...")

# --- CHANGED: XGBoost uses predict() directly, returning 0 (Normal) or 1 (Fraud) ---
# Isolation Forest used predict() returning -1/+1 and needed a sign-flip conversion.
# XGBoost already outputs the correct class labels (0 = Normal, 1 = Fraud),
# so no post-processing conversion is needed.
predictions = model.predict(X)

if y is not None:
    print("\nConfusion Matrix")
    print(confusion_matrix(y, predictions))

    print("\nClassification Report")
    print(classification_report(y, predictions, target_names=["Normal", "Fraud"]))