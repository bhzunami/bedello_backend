from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from app.controller import category_controller
from app.models import Category
from app.schemas import CategoryCreate, CategoryUpdate

from ..helpers import create_valid_category


def test_get_by_id() -> None:
    expected_category = create_valid_category()
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = expected_category
    category = category_controller.get_by_id(db, 1)
    assert category == expected_category
    print(db.method_calls)


def test_get_by_id_in_db(dbsession: Session) -> None:
    expected_category = create_valid_category()
    dbsession.add(expected_category)
    dbsession.commit()
    dbsession.refresh(expected_category)

    category = category_controller.get_by_id(dbsession, expected_category.id)
    assert category == expected_category


def test_get_by_wrong_id_in_db(dbsession: Session) -> None:
    expected_category = create_valid_category()
    dbsession.add(expected_category)
    dbsession.commit()
    dbsession.refresh(expected_category)

    category = category_controller.get_by_id(dbsession, expected_category.id + 2)
    assert category is None


def test_create_category(dbsession: Session) -> None:
    props = {"name": "Category Test", "sequence": 0}
    expected_category = CategoryCreate(**props)
    category = category_controller.create(db=dbsession, obj_in=expected_category)
    assert category.name == expected_category.name
    assert category.sequence == expected_category.sequence
    assert category.id == 1
    assert category.created_at is not None


def test_delete_category(dbsession: Session) -> None:
    expected_category = create_valid_category()
    dbsession.add(expected_category)
    dbsession.commit()
    dbsession.refresh(expected_category)

    category = category_controller.delete(db=dbsession, id=expected_category.id)
    assert category == expected_category

    deleted_category = category_controller.get_by_id(db=dbsession, id=expected_category.id)
    assert deleted_category is None


def test_get_all(dbsession: Session) -> None:
    for i in range(10):
        category = Category(name=f"Category {i}", sequence=i)
        dbsession.add(category)
    dbsession.commit()
    categories = category_controller.get_all(dbsession)
    assert len(categories) == 10


def test_update_category(dbsession: Session) -> None:
    existing_category = create_valid_category()
    print("asdfasdfasdfasdf")
    dbsession.add(existing_category)
    dbsession.commit()
    dbsession.refresh(existing_category)

    update_category = CategoryUpdate(
        id=existing_category.id, name=existing_category.name, sequence=5, description="Updated Category"
    )

    category: Category = category_controller.update(db=dbsession, db_obj=existing_category, obj_in=update_category)

    assert category.sequence == 5
    assert category.description == "Updated Category"
