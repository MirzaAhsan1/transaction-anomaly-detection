import numpy as np
import pandas as pd


CATEGORICAL_COLUMNS = [
    "currency",
    "transaction_type",
    "payment_method",
    "sender_bank",
    "receiver_bank",
    "merchant_category",
    "country",
    "browser",
    "operating_system",
    "device_type",
    "language",
    "timezone",
]

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Feature engineering for transaction data.

    This function is shared between:
    - Model training
    - Real-time prediction

    Always keep this file synchronized with the preprocessing pipeline.
    """

    df = df.copy()

    # ----------------------------------------------------
    # Transaction Time Features
    # ----------------------------------------------------

    if "transaction_time" in df.columns:
        df["transaction_time"] = pd.to_datetime(
            df["transaction_time"],
            errors="coerce"
        )

        df["transaction_hour"] = df["transaction_time"].dt.hour.fillna(0).astype(int)

        df["transaction_day"] = df["transaction_time"].dt.dayofweek.fillna(0).astype(int)

        df["is_weekend"] = (
            df["transaction_day"] >= 5
        ).astype(int)

    # ----------------------------------------------------
    # Amount Features
    # ----------------------------------------------------

    if "amount" in df.columns:
        df["amount"] = pd.to_numeric(
            df["amount"],
            errors="coerce"
        ).fillna(0)

        df["amount_log"] = np.log1p(df["amount"])

    # ----------------------------------------------------
    # Screen Features
    # ----------------------------------------------------

    if "screen_width" in df.columns:
        df["screen_width"] = pd.to_numeric(
            df["screen_width"],
            errors="coerce"
        ).fillna(0)

    if "screen_height" in df.columns:
        df["screen_height"] = pd.to_numeric(
            df["screen_height"],
            errors="coerce"
        ).fillna(0)

    if {
        "screen_width",
        "screen_height"
    }.issubset(df.columns):

        df["screen_area"] = (
            df["screen_width"]
            * df["screen_height"]
        )

    # ----------------------------------------------------
    # Device Features
    # ----------------------------------------------------

    if "device_type" in df.columns:

        df["is_mobile"] = (
            df["device_type"]
            .fillna("Unknown")
            .astype(str)
            .str.lower()
            .eq("mobile")
            .astype(int)
        )

    # ----------------------------------------------------
    # Normalize Categorical Features
    # ----------------------------------------------------

    for column in CATEGORICAL_COLUMNS:

        if column in df.columns:

            df[column] = (
                df[column]
                .fillna("Unknown")
                .astype(str)
                .str.lower()
                .str.strip()
            )

    # ----------------------------------------------------
    # Remove Unnecessary Columns
    # ----------------------------------------------------

    columns_to_drop = [

        # Original datetime
        "transaction_time",

        # High cardinality / unnecessary text
        "user_agent",
        "sender_name",
        "receiver_name",
        "sender_account_number",
        "receiver_account_number",
        "merchant_name",
        "ip_address",

        # Geo fields
        "city",
        "region",
        "latitude",
        "longitude",

        # Version fields
        "browser_version",
        "os_version",

    ]

    df.drop(
        columns=columns_to_drop,
        inplace=True,
        errors="ignore"
    )

    return df