from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, event
from sqlalchemy.orm import relationship

from app.db.base_class import Base, update_timestamps_before_insert, update_timestamps_before_update

if TYPE_CHECKING:
    from .product import Product  # noqa: F401
    from .property import Property  # noqa: F401


class ProductProperty(Base):
    product_id = Column(Integer, ForeignKey("product.id"), primary_key=True)
    property_id = Column(Integer, ForeignKey("property.id"), primary_key=True)
    product = relationship("Product", back_populates="properties")
    property = relationship("Property", back_populates="products")


event.listen(ProductProperty, "before_insert", update_timestamps_before_insert)
event.listen(ProductProperty, "before_update", update_timestamps_before_update)
