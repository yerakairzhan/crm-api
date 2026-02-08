import os
import sys
import uuid
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Ensure repo root is on sys.path for imports like `db`
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# Ensure tests use sqlite
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["SECRET_KEY"] = "test-secret"

from db import Base  # noqa: E402
from src.main import app  # noqa: E402
from db import get_db  # noqa: E402


@pytest.fixture()
def db_session():
    engine = create_engine(
        os.environ["DATABASE_URL"],
        connect_args={"check_same_thread": False},
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with engine.begin() as conn:
        conn.execute(text("PRAGMA foreign_keys=OFF"))
        # Drop in dependency order to avoid FK cycle warnings under SQLite
        conn.exec_driver_sql("DROP TABLE IF EXISTS comments")
        conn.exec_driver_sql("DROP TABLE IF EXISTS tasks")
        conn.exec_driver_sql("DROP TABLE IF EXISTS users")
        conn.execute(text("PRAGMA foreign_keys=ON"))
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def unique_email():
    return f"user_{uuid.uuid4().hex[:8]}@example.com"
