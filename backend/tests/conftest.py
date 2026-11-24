"""Shared pytest fixtures for isolated SwordAI backend tests."""

import sys
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool


BACKEND_DIRECTORY = Path(__file__).resolve().parents[1]

if str(BACKEND_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIRECTORY))

import app.models  # noqa: E402, F401 - registers all ORM models with Base.
from app.database.database import Base  # noqa: E402
from app.database.dependencies import get_db  # noqa: E402


@pytest.fixture
def test_engine() -> Generator[Engine, None, None]:
    """Provide an in-memory SQLite engine with the complete schema."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)

    try:
        yield engine
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture
def db_session(test_engine: Engine) -> Generator[Session, None, None]:
    """Provide a transaction-safe SQLAlchemy session for one test."""
    testing_session_local = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )
    session = testing_session_local()

    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def client(
    db_session: Session,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> Generator[TestClient, None, None]:
    """Provide a FastAPI client whose database dependency uses test storage."""
    # app.main creates tables against its module-level SQLite engine at import
    # time. Redirect that relative SQLite URL to pytest's temporary directory.
    monkeypatch.chdir(tmp_path)
    from app.main import app
    from app.database.database import engine as app_engine

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        app_engine.dispose()
