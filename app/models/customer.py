from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, Integer, String, event
from sqlalchemy.orm import relationship

from app.db.base_class import Base, update_timestamps_before_insert, update_timestamps_before_update

if TYPE_CHECKING:
    from .order import Order  # noqa: F401
    from .user import User  # noqa: F401


class Customer(Base):
    id = Column(Integer, primary_key=True, index=True)
    salutation = Column(String(50))
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    streetname = Column(String(100), nullable=False)
    address_additive = Column(String(50))
    zipcode = Column(String(4))
    city = Column(String(100))
    email = Column(String(255), unique=True)
    phone = Column(String(14))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    orders = relationship("Order", back_populates="customer", uselist=True)
    user = relationship("User", uselist=False, back_populates="customer")


event.listen(Customer, "before_insert", update_timestamps_before_insert)
event.listen(Customer, "before_update", update_timestamps_before_update)
