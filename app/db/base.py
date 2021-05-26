# Import all the models, so that Base has them before being imported by Alembic
# This is only used for Alembic
from app.db.base_class import Base  # noqa
from app.models.category import Category  # noqa
from app.models.customer import Customer  # noqa
from app.models.line_item import LineItem  # noqa
from app.models.order import Order  # noqa
from app.models.payment import Payment  # noqa
from app.models.product import Product  # noqa
from app.models.product_property import ProductProperty  # noqa
from app.models.property import Property  # noqa
from app.models.property_item import PropertyItem  # noqa
from app.models.shipment import Shipment  # noqa
from app.models.user import User  # noqa
