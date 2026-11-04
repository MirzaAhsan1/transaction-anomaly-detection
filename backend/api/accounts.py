from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.session import get_db
from models.bank_account import BankAccount

router = APIRouter(prefix="/accounts", tags=["Accounts"])


class AccountValidationResponse(BaseModel):
    exists: bool
    account_holder_name: str | None = None
    bank_name: str | None = None
    status: str | None = None


@router.get("/validate/{account_number}", response_model=AccountValidationResponse)
def validate_account(
    account_number: str,
    db: Session = Depends(get_db),
) -> AccountValidationResponse:
    account = (
        db.query(BankAccount)
        .filter(BankAccount.account_number == account_number)
        .first()
    )

    if account is None:
        return AccountValidationResponse(exists=False)

    return AccountValidationResponse(
        exists=True,
        account_holder_name=account.account_holder_name,
        bank_name=account.bank_name,
        status=account.status,
    )
