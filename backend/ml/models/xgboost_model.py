from xgboost import XGBClassifier


def build_model(scale_pos_weight: float = 1.0) -> XGBClassifier:
    """
    Creates and returns a configured XGBoost classifier.

    Parameters
    ----------
    scale_pos_weight : float
        Ratio of negative to positive samples (n_normal / n_fraud).
        This tells XGBoost to pay more attention to the minority (fraud) class,
        which is critical when the dataset is imbalanced.

        Example: if there are 43000 normal and 6000 fraud transactions,
        scale_pos_weight = 43000 / 6000 ≈ 6.9

    Returns
    -------
    XGBClassifier
        A ready-to-train XGBoost model.
    """

    model = XGBClassifier(
        # Number of boosting rounds (trees). More trees = better fit, slower training.
        n_estimators=300,

        # Maximum depth of each tree. Deeper = more complex patterns learned.
        max_depth=6,

        # Learning rate. Lower = more conservative steps, usually better generalization.
        learning_rate=0.1,

        # Fraction of features to use per tree (prevents overfitting).
        colsample_bytree=0.8,

        # Fraction of rows to use per tree (prevents overfitting).
        subsample=0.8,

        # Weight applied to fraud (positive) class to handle class imbalance.
        # Passed in from train.py based on actual label counts.
        scale_pos_weight=scale_pos_weight,

        # Use histogram-based tree method (fast and memory-efficient).
        tree_method="hist",

        # Binary classification: output probability of fraud (class 1).
        objective="binary:logistic",

        # Fix random seed for reproducibility.
        random_state=42,

        # Use all available CPU cores for training.
        n_jobs=-1,

        # Suppress verbose output during training.
        verbosity=0,
    )

    return model
