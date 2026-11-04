# Transaction Anomaly Detection Backend

This backend follows a clean layered structure for maintainability and professional project organization.

## Structure

- `app/` - FastAPI application entrypoint and runtime wiring
- `api/` - API router definitions
- `core/` - configuration, logging, and exception handling
- `schemas/` - request/response models
- `services/` - business logic services
- `src/` - ML pipeline, components, and model utilities
- `data/` - raw and processed datasets
- `artifacts/` - model artifacts
- `models/` - persisted model files
- `logs/` - application logs

## Run

```bash
cd backend
python -m uvicorn app.main:app --reload
```
