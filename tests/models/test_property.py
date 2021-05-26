from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import ProductProperty

from ..helpers import create_valid_category, create_valid_product, create_valid_property, create_valid_property_item


def test_property_create(dbsession: Session) -> None:
    property = create_valid_property()

    dbsession.add(property)
    dbsession.commit()
    dbsession.refresh(property)

    assert property.id is not None, "Id must be present"
    assert property.created_at is not None, "Created at was None, but should be set"
    assert property.updated_at is not None, "Updated at was None, but should be set"


def test_property_with_items(dbsession: Session) -> None:
    property = create_valid_property()
    property_item = create_valid_property_item(property)

    dbsession.add(property_item)
    dbsession.commit()
    dbsession.refresh(property_item)

    assert len(property.property_items) == 1, f"Length should be 1, got {len(property.property_items)}"
    assert property_item.id is not None, "Property item id should not be None"


def test_property_unique_name(dbsession: Session) -> None:
    property1 = create_valid_property()

    dbsession.add(property1)
    dbsession.commit()

    property2 = create_valid_property()
    dbsession.add(property2)
    try:
        dbsession.commit()
        assert False, "Property name must be unique"
    except IntegrityError:
        assert True, "Integrity Error expected"


def test_property_with_product(dbsession: Session) -> None:
    property = create_valid_property()
    property_item = create_valid_property_item(property)
    product = create_valid_product(create_valid_category())

    product_property = ProductProperty(property=property, product=product)

    property.products.append(product_property)
    dbsession.add(property_item)
    dbsession.commit()

    assert len(product.properties) == 1, "Properties must be present, but was not"
    assert len(property.products) == 1, "Product must be present, but was not"

    assert (
        product.properties[0].property.name == property.name
    ), f"Expected {property.name} got {product.properties[0].property.name}"

    assert (
        product.properties[0].property.property_items[0].name == property_item.name
    ), f"Expected {property_item.name} got {product.properties[0].property.property_items[0].name}"

    assert (
        property.products[0].product.name == product.name
    ), f"Expected {property.name} got {property.products[0].product.name}"
