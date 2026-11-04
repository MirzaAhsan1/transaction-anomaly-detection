from fastapi import APIRouter
from api.auth import router as auth_router
from api.transactions import router as transactions_router
from api.dashboard import router as dashboard_router
from api.receipt import router as receipt_router
from api.accounts import router as accounts_router

router = APIRouter(prefix="/api", tags=["anomaly"])

router.include_router(auth_router)
router.include_router(transactions_router)
router.include_router(dashboard_router)
router.include_router(receipt_router)
router.include_router(accounts_router)




@router.get("/predict")
def predict() -> dict[str, str]:
    return {"message": "Prediction endpoint scaffold ready."}

