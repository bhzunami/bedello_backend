from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..helpers import create_valid_category, create_valid_product


def test_product_create(dbsession: Session) -> None:
    category = create_valid_category()
    product = create_valid_product(category)

    dbsession.add(product)
    dbsession.commit()
    dbsession.refresh(product)

    assert product.id is not None, "Id must be present"
    assert product.created_at is not None, "Created at was None, but should be set"
    assert product.updated_at is not None, "Updated at was None, but should be set"
    assert product.active_from is not None, "Active from was None, but should be set"


def test_product_unique_name(dbsession: Session) -> None:
    category = create_valid_category()
    product1 = create_valid_product(category)
    dbsession.add(product1)
    dbsession.commit()

    product2 = create_valid_product(category)
    product2.number = 47
    dbsession.add(product2)
    try:
        dbsession.commit()
        assert False, "Product name must be unique"
    except Exception as ex:
        assert type(ex) == IntegrityError


def test_product_unique_number(dbsession: Session) -> None:
    category = create_valid_category()
    product1 = create_valid_product(category)
    dbsession.add(product1)
    dbsession.commit()

    product2 = create_valid_product(category)
    product2.name = "Test product 2"
    dbsession.add(product2)
    try:
        dbsession.commit()
        assert False, "Product number must be unique"
    except Exception as ex:
        assert type(ex) == IntegrityError
