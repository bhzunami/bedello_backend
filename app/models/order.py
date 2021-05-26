from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, Text, event
from sqlalchemy.orm import relationship

from app.db.base_class import Base, update_timestamps_before_insert, update_timestamps_before_update

if TYPE_CHECKING:
    from .customer import Customer  # noqa: F401
    from .line_item import LineItem  # noqa: F401
    from .payment import Payment  # noqa: F401
    from .shipment import Shipment  # noqa: F401


class Order(Base):
    id = Column(Integer, primary_key=True, index=True)
    distribution_number = Column(String(50), default=None)
    state = Column(String(100))  # State machine
    status = Column(String(100))
    total_price = Column(Float, nullable=False)
    pay_date = Column(Date, default=None)
    delivery_date = Column(Date, default=None)
    reminder_date = Column(Date, default=None)
    notes = Column(String(2048))
    pf_payment_method = Column(String(255), default=None)
    pf_acceptance = Column(String(255), default=None)
    pf_status = Column(String(255), default=None)
    pf_payid = Column(Text, default=None)
    pf_brand = Column(String(255), default=None)
    ip_address = Column(String(15))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # References
    line_items = relationship("LineItem", back_populates="order", uselist=True)
    payment_id = Column(Integer, ForeignKey("payment.id"))
    payment = relationship("Payment", back_populates="orders")
    shipment_id = Column(Integer, ForeignKey("shipment.id"))
    shipment = relationship("Shipment", back_populates="orders")
    customer_id = Column(Integer, ForeignKey("customer.id"))
    customer = relationship("Customer", back_populates="orders")


event.listen(Order, "before_insert", update_timestamps_before_insert)
event.listen(Order, "before_update", update_timestamps_before_update)
