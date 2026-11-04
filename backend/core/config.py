import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

load_dotenv()
@dataclass(frozen=True)
class Settings:
    app_name: str = "transaction-anomaly-detection"
    app_version: str = "1.0.0"
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    database_url: str = os.getenv("DATABASE_URL", "postgresql://postgres:Ahsan%4012@localhost/transaction-anomaly-detection")

    project_root: Path = PROJECT_ROOT
    backend_root: Path = BASE_DIR
    raw_data_dir: Path = BASE_DIR / "data" / "raw"
    processed_data_dir: Path = BASE_DIR / "data" / "processed"
    artifacts_dir: Path = BASE_DIR / "artifacts"
    models_dir: Path = BASE_DIR / "models"
    logs_dir: Path = BASE_DIR / "logs"

    # JWT Config
    jwt_secret: str = os.getenv("JWT_SECRET", "change-this-secret-in-production")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # SMTP Configuration
    smtp_host: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_username: str = os.getenv("SMTP_USERNAME", "")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "")
    smtp_from_email: str = os.getenv("SMTP_FROM_EMAIL", "")
    dummy_mode: bool = os.getenv("DUMMY_MODE", "false").lower() == "true"
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:...@localhost/transaction-anomaly-detection"
    )

@dataclass(frozen=True)
class PathConfig:
    project_root: Path = PROJECT_ROOT
    backend_root: Path = BASE_DIR
    raw_data_dir: Path = BASE_DIR / "data" / "raw"
    processed_data_dir: Path = BASE_DIR / "data" / "processed"
    artifacts_dir: Path = BASE_DIR / "artifacts"
    models_dir: Path = BASE_DIR / "models"
    logs_dir: Path = BASE_DIR / "logs"

@dataclass(frozen=True)
class DatasetConfig:
    dataset_name: str = "creditcard.csv"
    target_column: str = "Class"
    dataset_path: Path = BASE_DIR / "data" / "raw" / "creditcard.csv"

@dataclass(frozen=True)
class TrainingConfig:
    test_size: float = 0.2
    random_state: int = 42

@dataclass(frozen=True)
class ModelConfig:
    model_name: str = "fraud_detection_model.pkl"

settings = Settings()
paths = PathConfig()
dataset = DatasetConfig()
training = TrainingConfig()
model = ModelConfig()
