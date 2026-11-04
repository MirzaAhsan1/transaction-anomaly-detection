from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.base import Base
from db.session import engine
from models import User  # noqa: F401 — registers model
import sys

from api.routes import router as api_router
from core.config import settings
from api.auth import router as auth_router
import logging



logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(
    logging.Formatter("%(levelname)s:%(name)s:%(message)s")
)

logger.addHandler(handler)
logger.propagate = False


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Transaction anomaly detection backend service.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def root() -> dict[str, str]:
    return {"message": f"{settings.app_name} API"}
    
@app.on_event("startup")
def create_tables() -> None:
    if settings.dummy_mode:
        return

    Base.metadata.create_all(bind=engine)

app.include_router(api_router)
app.include_router(auth_router)

@app.get("/simulate-fraud-incident")
def simulate_fraud_incident():
    logger.error("Payment processing failed: transaction service returned 500")

    return {
        "status": "error",
        "message": "Simulated payment processing failure"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host=settings.host, port=settings.port, reload=settings.reload)