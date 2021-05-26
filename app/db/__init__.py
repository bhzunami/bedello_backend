from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    try:
        db = LocalSession()
        yield db
    finally:
        db.close()
