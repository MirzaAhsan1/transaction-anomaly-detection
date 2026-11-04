from core.logging import logger


class PredictionService:
    """Service layer for anomaly detection predictions."""

    def __init__(self) -> None:
        logger.info("Prediction service initialized")

    def predict(self, payload: dict) -> dict:
        logger.info("Prediction request received")
        return {
            "transaction_id": payload.get("transaction_id"),
            "is_anomalous": False,
            "risk_score": 0.0,
        }
