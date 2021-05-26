from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, Text, event
from sqlalchemy.orm import relationship

from app.db.base_class import Base, update_timestamps_before_insert, update_timestamps_before_update

if TYPE_CHECKING:
    from .category import Category  # noqa: F401
    from .line_item import LineItem  # noqa: F401
    from .product_property import ProductProperty  # noqa: F401


class Product(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    number = Column(Integer, unique=True, nullable=False)
    price = Column(Float)
    active_until = Column(Date, default=None)
    active_from = Column(Date, default=datetime.utcnow().date)
    sale_price = Column(Float, default=None)
    sale_from = Column(Date, default=None)
    sale_until = Column(Date, default=None)
    num_in_stock = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", back_populates="products")
    properties = relationship("ProductProperty", back_populates="product", uselist=True)
    line_items = relationship("LineItem", back_populates="product", uselist=True)


event.listen(Product, "before_insert", update_timestamps_before_insert)
event.listen(Product, "before_update", update_timestamps_before_update)
