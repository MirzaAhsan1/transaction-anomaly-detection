import sys
from pathlib import Path

# Add backend directory to path so we can import from core and db
sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy import text
from db.session import engine

def migrate():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE transactions ADD COLUMN prediction VARCHAR(20)"))
            print("Added column 'prediction'")
        except Exception as e:
            print(f"Skipped 'prediction': {e}")
            
        try:
            conn.execute(text("ALTER TABLE transactions ADD COLUMN risk_score FLOAT"))
            print("Added column 'risk_score'")
        except Exception as e:
            print(f"Skipped 'risk_score': {e}")
            
        try:
            conn.execute(text("ALTER TABLE transactions ADD COLUMN confidence_score FLOAT"))
            print("Added column 'confidence_score'")
        except Exception as e:
            print(f"Skipped 'confidence_score': {e}")
            
        try:
            conn.execute(text("ALTER TABLE transactions ADD COLUMN model_version VARCHAR(20)"))
            print("Added column 'model_version'")
        except Exception as e:
            print(f"Skipped 'model_version': {e}")

        conn.commit()
    print("Migration finished.")

if __name__ == "__main__":
    migrate()
