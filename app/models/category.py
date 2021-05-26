from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, Integer, String, Text, event
from sqlalchemy.orm import relationship

from app.db.base_class import Base, update_timestamps_before_insert, update_timestamps_before_update

if TYPE_CHECKING:
    from .product import Product  # noqa: F401


class Category(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(Text)
    sequence = Column(Integer, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    products = relationship("Product", back_populates="category", uselist=True)


event.listen(Category, "before_insert", update_timestamps_before_insert)
event.listen(Category, "before_update", update_timestamps_before_update)
