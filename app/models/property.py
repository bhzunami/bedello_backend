from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, Integer, String, Text, event
from sqlalchemy.orm import relationship

from app.db.base_class import Base, update_timestamps_before_insert, update_timestamps_before_update

if TYPE_CHECKING:
    from .product_property import ProductProperty  # noqa: F401
    from .property_item import PropertyItem  # noqa: F401


class Property(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, default=None)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    property_items = relationship("PropertyItem", back_populates="property", uselist=True)
    products = relationship("ProductProperty", back_populates="property", uselist=True)


event.listen(Property, "before_insert", update_timestamps_before_insert)
event.listen(Property, "before_update", update_timestamps_before_update)
