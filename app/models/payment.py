from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, Float, Integer, String, event
from sqlalchemy.orm import relationship

from app.db.base_class import Base, update_timestamps_before_insert, update_timestamps_before_update

if TYPE_CHECKING:
    from .order import Order  # noqa: F401


class Payment(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(1024))
    additional_costs = Column(Float, default=None)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    orders = relationship("Order", back_populates="payment", uselist=True)


event.listen(Payment, "before_insert", update_timestamps_before_insert)
event.listen(Payment, "before_update", update_timestamps_before_update)
