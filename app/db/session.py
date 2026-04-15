import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL

if not DATABASE_URL:
    raise Exception("DATABASE_URL is not set")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

def create_db_engine_with_retry():
    for i in range(10):
        try:
            engine = create_engine(DATABASE_URL)
            conn = engine.connect()
            conn.close()
            return engine
        except Exception as e:
            print(f"DB not ready, retrying... ({i})")
            time.sleep(2)

    raise Exception("DB never became ready")

engine = create_db_engine_with_retry()
SessionLocal = sessionmaker(bind=engine)