from typing import Any, Dict

from pydantic import ValidationError

from app.schemas import Category, CategoryCreate, CategoryUpdate


def test_category_create() -> None:
    name: str = "Category Test"
    sequence: int = 0
    category: CategoryCreate = CategoryCreate(name=name, sequence=sequence)

    assert category.created_at is not None, "Created at should be filled out"
    assert category.updated_at is not None, "Updated at should be filled out"


def test_category_update() -> None:
    props: Dict[str, Any] = {
        "name": "Category Test",
        "sequence": 1,
        "id": 5,
        "updated_at": "2020-08-15T14:33:30.625578",
        "created_at": "2020-08-15T14:33:30.625578",
    }

    category: CategoryUpdate = CategoryUpdate(**props)
    assert category is not None


def test_category_update_missing_id() -> None:
    props: Dict[str, Any] = {
        "name": "Category Test",
        "sequence": 1,
        "updated_at": "2020-08-15T14:33:30.625578",
        "created_at": "2020-08-15T14:33:30.625578",
    }

    try:
        CategoryUpdate(**props)
        assert False, "Id must be present in update"
    except ValidationError as ex:
        assert ex.errors() == [{"loc": ("id",), "msg": "field required", "type": "value_error.missing"}]


def test_category_orm() -> None:
    props: Dict[str, Any] = {
        "id": 1,
        "name": "Category Test",
        "sequence": 1,
        "updated_at": "2020-08-15T14:33:30.625578",
        "created_at": "2020-08-15T14:33:30.625578",
    }
    category: Category = Category(**props)
    assert category.created_at is not None, "Created at should be filled out"
    assert category.updated_at is not None, "Updated at should be filled out"
