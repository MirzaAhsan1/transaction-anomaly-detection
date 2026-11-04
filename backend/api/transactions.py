import random
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi import Request
from ml.services.predictor import predict_transaction

from core.config import settings
from db.session import get_db
from models.user import User
from models.bank_account import BankAccount
from models.transaction import Transaction
from schemas.transaction import TransactionCreate, TransactionResponse
from services.device_service import get_client_ip
from services.geo_service import resolve_ip as get_location
from services.email_service import send_transaction_email

router = APIRouter(prefix="/transactions", tags=["transactions"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")
        
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

@router.post("/", response_model=TransactionResponse)
def create_transaction(
    request: Request,
    payload: TransactionCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # ── Account Validation Guard ──────────────────────────────────────────
    # Backend is the source of truth. Validate BEFORE ML, DB, or email.
    sender_account = (
        db.query(BankAccount)
        .filter(BankAccount.account_number == payload.sender_account_number)
        .first()
    )
    if not sender_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sender account not found",
        )

    receiver_account = (
        db.query(BankAccount)
        .filter(BankAccount.account_number == payload.receiver_account_number)
        .first()
    )
    if not receiver_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Receiver account not found",
        )
    # ─────────────────────────────────────────────────────────────────────

    transaction_data = payload.model_dump()
    prediction = predict_transaction(transaction_data)

    ip = get_client_ip(request)
    try:
        location = get_location(ip)
    except Exception:
        location = {}

    transaction_data.update({
        "ip_address": ip,
        "country": location["country"],
        "city": location["city"],
        "region": location["region"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
    })


    transaction = Transaction(
        user_id=current_user.id,
        prediction=prediction["prediction"],
        risk_score=float(prediction["risk_score"]),
        confidence_score=float(prediction["confidence_score"]),
        action=prediction["action"],
        model_version=prediction.get("model_version"),
        **transaction_data
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    
    background_tasks.add_task(send_transaction_email, transaction, current_user.email)

    return transaction

@router.get("/", response_model=list[TransactionResponse])
def get_transactions(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    transactions = db.query(Transaction).filter(Transaction.user_id == current_user.id).order_by(Transaction.created_at.desc()).offset(skip).limit(limit).all()
    return transactions
