from datetime import datetime
from pydantic import BaseModel, Field

class TransactionCreate(BaseModel):
    amount: float = Field(..., gt=0)
    currency: str = Field(..., max_length=10)
    transaction_type: str = Field(..., max_length=50)
    payment_method: str = Field(..., max_length=50)
    transaction_time: datetime

    sender_name: str = Field(..., max_length=100)
    sender_account_number: str = Field(..., max_length=50)
    sender_bank: str = Field(..., max_length=100)

    receiver_name: str = Field(..., max_length=100)
    receiver_account_number: str = Field(..., max_length=50)
    receiver_bank: str = Field(..., max_length=100)

    merchant_name: str = Field(..., max_length=100)
    merchant_category: str = Field(..., max_length=100)

    browser: str = Field(..., max_length=80)
    browser_version: str = Field(..., max_length=30)

    operating_system: str = Field(..., max_length=80)
    os_version: str = Field(..., max_length=30)

    device_type: str = Field(..., max_length=80)

    language: str = Field(..., max_length=20)
    timezone: str = Field(..., max_length=80)

    screen_width: int
    screen_height: int

    user_agent: str

class TransactionResponse(BaseModel):
    id: int
    transaction_id: str
    user_id: int
    amount: float
    currency: str
    transaction_type: str
    payment_method: str
    transaction_time: datetime
    sender_name: str
    sender_account_number: str
    sender_bank: str
    receiver_name: str
    receiver_account_number: str
    receiver_bank: str
    merchant_name: str
    merchant_category: str

    # Geo Information
    country: str
    city: str
    region: str | None = None
    latitude: float | None = None
    longitude: float | None = None

    # Network Information
    ip_address: str

    # Device Information
    browser: str
    browser_version: str

    operating_system: str
    os_version: str

    device_type: str

    language: str
    timezone: str

    screen_width: int
    screen_height: int

    user_agent: str

    # ML Result
    prediction: str | None = None
    risk_score: float | None = None
    confidence_score: float | None = None
    action: str | None = None
    model_version: str | None = None

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

