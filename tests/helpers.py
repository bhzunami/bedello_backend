from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from app.models import Category, LineItem, Payment, Product, ProductProperty, Property, PropertyItem, Shipment


def create_valid_category() -> Category:
    props = {"name": "Test Category", "description": "This is a test category", "sequence": 1}
    category = Category(**props)
    return category


def create_valid_product(category: Category) -> Product:
    props = {
        "name": "Test Product",
        "description": "Description for the Test product",
        "number": 1,
        "price": 20.00,
        "active_until": None,
        "active_from": datetime.now(),
        "num_in_stock": 3,
        "category": category,
    }
    return Product(**props)


def create_valid_shipment() -> Shipment:
    props = {"name": "per Post", "additional_costs": 20.00, "days_to_deliver": 2}
    return Shipment(**props)


def create_valid_payment() -> Payment:
    props = {"name": "Vorauskasse", "additional_costs": 20.00}
    return Payment(**props)


def create_valid_line_item(product: Product) -> LineItem:
    props = {"quantity": 1, "product": product}
    return LineItem(**props)


def create_valid_property(propertyItems: List[PropertyItem] = []) -> Property:
    props = {"name": "Test Property", "description": "Property description", "property_items": propertyItems}
    return Property(**props)


def create_valid_property_item(property: Property = None) -> PropertyItem:
    props = {"name": "Red", "description": "The color red", "item_order": 1, "property": property}
    return PropertyItem(**props)


def setup_store(dbsession: Session) -> None:
    # Properties
    color_red = PropertyItem(name="red", description="The color red", item_order=1)
    color_green = PropertyItem(name="green", description="The color green", item_order=2)
    color_blue = PropertyItem(name="blue", description="The color blue", item_order=3)
    property_items = [color_red, color_green, color_blue]

    color_property = Property(name="Color", description="Specific color", property_items=property_items)
    dbsession.add(color_property)

    # Categories
    shirts = Category(name="T-shirts", description="Everything that has short sleeves", sequence=1)
    hats = Category(name="Hats", description="Everything you put on your head", sequence=2)
    dbsession.add(shirts)
    dbsession.add(hats)

    # shipment
    by_mail = Shipment(name="Mail", description="The traditional mail", additional_costs=0, days_to_deliver=2)
    express = Shipment(name="Express-Mail", description="The fast mail", additional_costs=5, days_to_deliver=1)
    dbsession.add(by_mail)
    dbsession.add(express)

    # payments
    credit_card = Payment(name="Credit-Card", description="Swipe it", additional_costs=10)
    dbsession.add(credit_card)

    # Products
    base_cap = Product(
        name="Base cap", description="The best cap in twon", number=100, price=25.55, num_in_stock=10, category=hats
    )
    base_cap_properties = ProductProperty(property=color_property)
    base_cap.properties.append(base_cap_properties)
    dbsession.add(base_cap)

    shirt1 = Product(name="Shirt 1", description="Shirt #1", number=200, price=30.55, num_in_stock=23, category=shirts)
    shirt1_properties = ProductProperty(property=color_property, product=shirt1)
    shirt1.properties.append(shirt1_properties)
    dbsession.add(shirt1)

    shirt2 = Product(name="Shirt 2", description="Shirt #2", number=201, price=15.5, num_in_stock=2, category=shirts)
    shirt_properties2 = ProductProperty(property=color_property, product=shirt2)
    shirt2.properties.append(shirt_properties2)
    dbsession.add(shirt2)

    dbsession.commit()
