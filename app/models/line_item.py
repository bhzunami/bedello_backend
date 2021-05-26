from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, event
from sqlalchemy.orm import relationship

from app.db.base_class import Base, update_timestamps_before_insert, update_timestamps_before_update

if TYPE_CHECKING:
    from .order import Order  # noqa: F401
    from .product import Product  # noqa: F401


class LineItem(Base):
    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    product = relationship("Product", back_populates="line_items")

    order_id = Column(Integer, ForeignKey("order.id"))
    order = relationship("Order", back_populates="line_items")


event.listen(LineItem, "before_insert", update_timestamps_before_insert)
event.listen(LineItem, "before_update", update_timestamps_before_update)
