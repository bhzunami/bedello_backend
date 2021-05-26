from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, event
from sqlalchemy.orm import relationship

from app.db.base_class import Base, update_timestamps_before_insert, update_timestamps_before_update

if TYPE_CHECKING:
    from .customer import Customer  # noqa: F401


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    login_name = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    remember_token = Column(Integer)
    is_admin = Column(Integer)
    state = Column(String(50))
    password_reset_token = Column(String(255))
    password_reset_token_sent_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    customer = relationship("Customer", back_populates="user")


event.listen(User, "before_insert", update_timestamps_before_insert)
event.listen(User, "before_update", update_timestamps_before_update)
