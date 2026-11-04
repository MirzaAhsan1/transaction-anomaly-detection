from pathlib import Path
import joblib
import pandas as pd

# --- CHANGED: import XGBoost model builder instead of Isolation Forest ---
from ml.models.xgboost_model import build_model

# Preprocessing pipeline is unchanged — reused as-is
from ml.preprocessing.preprocessing import prepare_training_data


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET = BASE_DIR / "datasets" / "generated_transactions.csv"

ARTIFACT_DIR = BASE_DIR / "artifacts"
ARTIFACT_DIR.mkdir(exist_ok=True)

print("Loading dataset...")

df = pd.read_csv(DATASET)

print(f"Dataset Shape : {df.shape}")

# -----------------------------------
# Preprocessing (unchanged)
# -----------------------------------

print("Preparing training data...")
X, y = prepare_training_data(df)

# -----------------------------------
# Class Imbalance Handling
# -----------------------------------

# XGBoost is a supervised model — it needs labels (y).
# Unlike Isolation Forest, it learns directly from fraud vs normal examples.
#
# Because fraud is rare (~12% of data), we compute scale_pos_weight to
# tell XGBoost to treat fraud cases as more important during training.
#
# Formula: scale_pos_weight = count(normal) / count(fraud)

if y is not None:
    n_normal = (y == 0).sum()
    n_fraud  = (y == 1).sum()
    scale_pos_weight = n_normal / n_fraud

    print(f"Normal transactions : {n_normal}")
    print(f"Fraud  transactions : {n_fraud}")
    print(f"scale_pos_weight    : {scale_pos_weight:.2f}")
else:
    # Fallback: assume balanced classes if no label column
    scale_pos_weight = 1.0
    print("Warning: 'label' column not found — using scale_pos_weight=1.0")

# -----------------------------------
# Build & Train Model
# -----------------------------------

print("Building model...")
model = build_model(scale_pos_weight=scale_pos_weight)

print("Training model...")
# --- CHANGED: XGBoost is supervised, so we pass both X and y ---
model.fit(X, y)

# -----------------------------------
# Save Artifacts
# -----------------------------------

# --- CHANGED: save as xgboost_model.pkl (different filename than Isolation Forest) ---
model_path = ARTIFACT_DIR / "xgboost_model.pkl"
joblib.dump(model, model_path)

print()
print("Training Complete")
print(f"Model Saved -> {model_path}")