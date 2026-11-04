from pathlib import Path
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

from ml.preprocessing.feature_engineering import engineer_features, CATEGORICAL_COLUMNS


BASE_DIR = Path(__file__).resolve().parent.parent

ARTIFACT_DIR = BASE_DIR / "artifacts"
ARTIFACT_DIR.mkdir(exist_ok=True)

LABEL_ENCODERS_FILE = ARTIFACT_DIR / "label_encoders.pkl"
FEATURE_COLUMNS_FILE = ARTIFACT_DIR / "feature_columns.pkl"


def prepare_training_data(df: pd.DataFrame):
    """
    Prepare dataset for model training.

    Steps
    -----
    1. Feature Engineering
    2. Separate X and y
    3. Fit LabelEncoders for categorical features
    4. Save encoders and feature order
    """

    df = engineer_features(df)

    if "label" in df.columns:
        y = df["label"]
    else:
        y = None

    X = df.drop(
        columns=[
            "label",
            "risk_score",
        ],
        errors="ignore",
    )

    label_encoders = {}

    for column in CATEGORICAL_COLUMNS:
        if column in X.columns:
            X[column] = X[column].fillna("unknown").astype(str)
            
            le = LabelEncoder()
            X[column] = le.fit_transform(X[column])
            label_encoders[column] = le

    joblib.dump(label_encoders, LABEL_ENCODERS_FILE)
    
    joblib.dump(X.columns.tolist(), FEATURE_COLUMNS_FILE)

    return X, y


def prepare_inference_data(df: pd.DataFrame, label_encoders: dict, feature_columns: list):
    """
    Prepare data for real-time prediction or evaluation.
    
    Steps
    -----
    1. Feature Engineering
    2. Apply LabelEncoders, handling unseen categories
    3. Ensure column order matches training exactly
    """
    df = engineer_features(df)
    
    df = df.drop(
        columns=[
            "label",
            "risk_score",
        ],
        errors="ignore",
    )
    
    for column, le in label_encoders.items():
        if column in df.columns:
            df[column] = df[column].fillna("unknown").astype(str)
            
            known_classes = set(le.classes_)
            
            fallback_class = "unknown" if "unknown" in known_classes else le.classes_[0]
            
            df[column] = df[column].apply(lambda x: x if x in known_classes else fallback_class)
            
            df[column] = le.transform(df[column])
            
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0
            
    X = df[feature_columns]
    
    return X