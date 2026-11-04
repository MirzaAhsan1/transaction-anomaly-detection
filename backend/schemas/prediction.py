from pydantic import BaseModel, Field


class TransactionInput(BaseModel):
    transaction_id: str = Field(..., description="Unique transaction identifier")
    amount: float = Field(..., description="Transaction amount")
    merchant: str = Field(..., description="Merchant name")


class PredictionResponse(BaseModel):
    transaction_id: str
    is_anomalous: bool
    risk_score: float
