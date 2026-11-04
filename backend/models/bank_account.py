from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from db.base import Base


class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, index=True)

    account_number = Column(String(20), unique=True, nullable=False, index=True)

    account_holder_name = Column(String(100), nullable=False)

    bank_name = Column(String(100), nullable=False)

    account_type = Column(String(50), default="Savings")

    balance = Column(Float, default=0.0)

    status = Column(String(20), default="Active")

    created_at = Column(DateTime(timezone=True), server_default=func.now())