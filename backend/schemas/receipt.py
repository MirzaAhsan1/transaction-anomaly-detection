from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ReceiptParseResult(BaseModel):
    # Map the extracted receipt fields into the NewTransaction form shape
    amount: Optional[float] = Field(default=None, gt=0)
    currency: Optional[str] = Field(default=None, max_length=10)

    # Optional fields (receipt format differs)
    transaction_time: Optional[datetime] = None

    sender_name: Optional[str] = Field(default=None, max_length=100)
    sender_account_number: Optional[str] = Field(default=None, max_length=50)
    sender_bank: Optional[str] = Field(default=None, max_length=100)

    receiver_name: Optional[str] = Field(default=None, max_length=100)
    receiver_account_number: Optional[str] = Field(default=None, max_length=50)
    receiver_bank: Optional[str] = Field(default=None, max_length=100)

    merchant_name: Optional[str] = Field(default=None, max_length=100)
    merchant_category: Optional[str] = Field(default=None, max_length=100)

    payment_method: Optional[str] = Field(default=None, max_length=50)
    transaction_type: Optional[str] = Field(default=None, max_length=50)

    # Parsing metadata
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    extraction_method: str = Field(default="regex", max_length=50)
    bank_detected: Optional[str] = Field(default=None, max_length=100)
    raw_text_preview: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)

