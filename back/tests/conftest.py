# tests/conftest.py
import os
import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app_factory import create_app
from datetime import datetime, timezone, timedelta
from dbconfig.conn import get_dbconn
from dbconfig.base import Base
from models.schemas import Keys
from lib.api_validation import validate_api_key

def make_test_engine():
    test_env = os.getenv("TEST_ENV", "mock")

    if test_env == "mock":
        TEST_DATABASE_URL = "sqlite:///./test.db"
        return create_engine(
            TEST_DATABASE_URL,
            connect_args={"check_same_thread": False},
        )

    if test_env == "sandbox":
        sandbox_conn_str = os.getenv("SANDBOX_CONNECTION_STRING")
        if not sandbox_conn_str:
            raise RuntimeError("Invalid env.var SANDBOX_CONNECTION_STRING: connection string is not set")

        return create_engine(sandbox_conn_str)

    raise RuntimeError(f"Invalid env.var TEST_ENV: {test_env}. It must be either 'mock' or 'sandbox'")


@pytest.fixture(scope="session")
def db_engine():
    engine = make_test_engine()
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()

    SessionTesting = sessionmaker(
        bind=connection,
        autoflush=False,
        autocommit=False,
    )

    session = SessionTesting()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def client(db_session):
    app = create_app()

    def override_get_dbconn():
        yield db_session

    def override_validate_api_key():
        return Keys(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            key_text=uuid.uuid4(),
            is_revoked=False,
            expires_at_tmzone=datetime.now(timezone.utc),
            created_at_tmzone=datetime.now(timezone.utc) + timedelta(days=365)
        )

    app.dependency_overrides[get_dbconn] = override_get_dbconn
    app.dependency_overrides[validate_api_key] = override_validate_api_key

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
