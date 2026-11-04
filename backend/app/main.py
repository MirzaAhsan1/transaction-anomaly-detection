from fastapi import FastAPI

from ..api.routes import router as api_router
from ..core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Transaction anomaly detection backend service.",
)

app.include_router(api_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.app.main:app", host=settings.host, port=settings.port, reload=settings.reload)
