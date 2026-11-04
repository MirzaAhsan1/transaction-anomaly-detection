from sklearn.ensemble import IsolationForest


def build_model() -> IsolationForest:
    """
    Creates and returns a configured Isolation Forest model.
    """

    model = IsolationForest(
        n_estimators=200,
        contamination=0.0017,
        max_samples="auto",
        random_state=42,
        n_jobs=-1,
    )

    return model