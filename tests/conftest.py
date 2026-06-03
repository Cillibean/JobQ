import os
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEST_DB_PATH = Path(__file__).resolve().parent / "test_jobq.sqlite3"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

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
