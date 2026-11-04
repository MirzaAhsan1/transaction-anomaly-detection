import pandas as pd


FEATURE_COLUMNS = [
    "Time",
    "Amount",
]

FEATURE_COLUMNS.extend(
    [f"V{i}" for i in range(1, 29)]
)


TARGET_COLUMN = "Class"


def prepare_training_data(df: pd.DataFrame):
    """
    Splits dataframe into features and labels.
    """

    X = df[FEATURE_COLUMNS].copy()

    y = df[TARGET_COLUMN].copy()

    return X, y