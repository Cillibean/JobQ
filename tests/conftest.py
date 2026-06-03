import os
from pathlib import Path

import pytest


TEST_DB_PATH = Path(__file__).resolve().parent / "test_jobq.sqlite3"

os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH}"
os.environ["REDIS_URL"] = "redis://localhost:6379/0"

from app.db.models import Base
from app.db.session import engine, get_session_local


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    Session = get_session_local()
    with Session() as db:
        yield db
