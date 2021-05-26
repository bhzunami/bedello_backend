from datetime import datetime
from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


def update_timestamps_before_insert(mapper: Any, connection: Any, target: Any) -> None:
    ts = datetime.utcnow()
    target.created_at = ts
    target.updated_at = ts


def update_timestamps_before_update(mapper: Any, connection: Any, target: Any) -> None:
    target.updated_at = datetime.utcnow()
