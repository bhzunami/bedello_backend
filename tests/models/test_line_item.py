from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..helpers import create_valid_category, create_valid_line_item, create_valid_product


def test_lineItem_create(dbsession: Session) -> None:
    category = create_valid_category()
    product = create_valid_product(category)
    lineItem = create_valid_line_item(product)

    dbsession.add(lineItem)
    dbsession.commit()
    dbsession.refresh(lineItem)

    assert lineItem.id is not None, "Id must be present"
    assert lineItem.created_at is not None, "Created at was None, but should be set"
    assert lineItem.updated_at is not None, "Updated at was None, but should be set"


def test_lineItem_default_value(dbsession: Session) -> None:
    category = create_valid_category()
    product = create_valid_product(category)
    lineItem = create_valid_line_item(product)
    lineItem.quantity = None  # type: ignore

    dbsession.add(lineItem)
    dbsession.commit()
    dbsession.refresh(lineItem)

    assert lineItem.quantity == 1, f"Default quanitiy value should be one got {lineItem.quantity}"


def test_lineItem_without_product(dbsession: Session) -> None:
    category = create_valid_category()
    product = create_valid_product(category)
    lineItem = create_valid_line_item(product)
    lineItem.product = None  # type: ignore

    dbsession.add(lineItem)
    try:
        dbsession.commit()
        assert False, "Line item needs to have a product"
    except Exception as ex:
        assert type(ex) == IntegrityError
