from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, event
from sqlalchemy.orm import relationship

from app.db.base_class import Base, update_timestamps_before_insert, update_timestamps_before_update

if TYPE_CHECKING:
    from .property import Property  # noqa: F401


class PropertyItem(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, default=None)
    item_order = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    property_id = Column(Integer, ForeignKey("property.id"), nullable=False)
    property = relationship("Property", back_populates="property_items")


event.listen(PropertyItem, "before_insert", update_timestamps_before_insert)
event.listen(PropertyItem, "before_update", update_timestamps_before_update)
