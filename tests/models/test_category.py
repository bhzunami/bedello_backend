from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Category

from ..helpers import create_valid_category, create_valid_product


def test_category_create(dbsession: Session) -> None:
    category: Category = create_valid_category()

    dbsession.add(category)
    dbsession.commit()
    dbsession.refresh(category)

    assert category.id is not None, "Id must be present"
    assert category.created_at is not None, "Created at was None, but should be set"
    assert category.updated_at is not None, "Updated at was None, but should be set"


def test_category_unique_name(dbsession: Session) -> None:
    category1: Category = create_valid_category()
    dbsession.add(category1)
    dbsession.commit()

    category2 = create_valid_category()
    dbsession.add(category2)
    try:
        dbsession.commit()
        assert False, "Name must be unique"
    except Exception as ex:
        assert type(ex) == IntegrityError


def test_category_unique_sequence(dbsession: Session) -> None:
    category1: Category = create_valid_category()
    dbsession.add(category1)
    dbsession.commit()

    category2: Category = create_valid_category()
    category2.name = "Test_Category2"
    dbsession.add(category2)
    try:
        dbsession.commit()
        assert False, "Sequence must be unique"
    except Exception as ex:
        assert type(ex) == IntegrityError


def test_category_name_present(dbsession: Session) -> None:
    description: str = "This is a test category"
    category = Category(description=description, sequence=1)
    dbsession.add(category)
    try:
        dbsession.commit()
        assert False, "Name must be present"
    except Exception as ex:
        assert type(ex) == IntegrityError


def test_category_with_product(dbsession: Session) -> None:
    category: Category = create_valid_category()
    product = create_valid_product(category)

    dbsession.add(product)
    dbsession.commit()

    dbsession.add(category)
    dbsession.commit()
    dbsession.refresh(category)
    assert len(category.products) == 1, "Product must be assigned to category"  # type: ignore[arg-type]
    assert category.products[0].name == product.name, "Product must be assigned to category"  # type: ignore[index]
