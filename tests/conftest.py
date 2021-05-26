from typing import Any, Generator

import pytest  # type: ignore

# from starlette.testclient import TestClient
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.base import Base
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test.db"


@pytest.fixture(scope="module")
def test_app() -> Generator[TestClient, None, None]:
    client = TestClient(app)
    yield client  # testing happens here


@pytest.fixture(scope="session")
def engine() -> Any:
    return create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)


@pytest.fixture(scope="session")
def tables(engine: Any) -> Any:
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def dbsession(engine: Any, tables: Any) -> Any:
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = Session(bind=connection)
    # session = sessionmaker(bind=db_engine)

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()
