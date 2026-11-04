from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    transaction_id: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=False,
        default=lambda: f"TXN_{uuid4().hex[:8].upper()}",
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False)
    transaction_type: Mapped[str] = mapped_column(String(50), nullable=False)
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)
    transaction_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    sender_name: Mapped[str] = mapped_column(String(100), nullable=False)
    sender_account_number: Mapped[str] = mapped_column(String(50), nullable=False)
    sender_bank: Mapped[str] = mapped_column(String(100), nullable=False)

    receiver_name: Mapped[str] = mapped_column(String(100), nullable=False)
    receiver_account_number: Mapped[str] = mapped_column(String(50), nullable=False)
    receiver_bank: Mapped[str] = mapped_column(String(100), nullable=False)

    merchant_name: Mapped[str] = mapped_column(String(100), nullable=False)
    merchant_category: Mapped[str] = mapped_column(String(100), nullable=False)

    # Geo Information
    country: Mapped[str] = mapped_column(String(80), nullable=False)
    city: Mapped[str] = mapped_column(String(80), nullable=False)
    region: Mapped[str | None] = mapped_column(String(80), nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Network
    ip_address: Mapped[str] = mapped_column(String(50), nullable=False)

    # Device
    browser: Mapped[str] = mapped_column(String(80), nullable=False)
    browser_version: Mapped[str] = mapped_column(String(30), nullable=False)

    operating_system: Mapped[str] = mapped_column(String(80), nullable=False)
    os_version: Mapped[str] = mapped_column(String(30), nullable=False)

    device_type: Mapped[str] = mapped_column(String(50), nullable=False)

    language: Mapped[str] = mapped_column(String(20), nullable=False)
    timezone: Mapped[str] = mapped_column(String(100), nullable=False)

    screen_width: Mapped[int] = mapped_column(nullable=False)
    screen_height: Mapped[int] = mapped_column(nullable=False)

    user_agent: Mapped[str] = mapped_column(String(500), nullable=False)

    # ML Result
    prediction: Mapped[str | None] = mapped_column(String(20), nullable=True)
    risk_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    confidence_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    action: Mapped[str | None] = mapped_column(String(80), nullable=True)
    model_version: Mapped[str | None] = mapped_column(String(20), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="transactions")

