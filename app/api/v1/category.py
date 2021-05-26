import logging
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import db, schemas
from app.controller import category_controller

router = APIRouter()


logger = logging.getLogger(__name__)


@router.get("/", response_model=List[schemas.Category])
def get(db: Session = Depends(db.get_db), skip: int = 0, limit: int = 100) -> Any:
    """
    Get all categries
    """
    return category_controller.get_all(db=db, skip=skip, limit=limit)


@router.get("/{id}", response_model=schemas.Category)
def show(*, db: Session = Depends(db.get_db), id: int) -> Any:
    """
    Get category by id
    """
    category = category_controller.get_by_id(db=db, id=id)
    if not category:
        raise HTTPException(status_code=404, detail=f"Category with id {id} does not exist")
    return category


@router.put("/{id}", response_model=schemas.Category)
def update(*, db: Session = Depends(db.get_db), id: int, category_in: schemas.CategoryUpdate,) -> Any:
    """Update a exiting category.

    item = crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item = crud.item.update(db=db, db_obj=item, obj_in=item_in)
    return item
    """
    category = category_controller.get_by_id(db=db, id=id)
    if not category:
        raise HTTPException(status_code=404, detail=f"Category with id {id}, does not exist")
    category = category_controller.update(db=db, db_obj=category, obj_in=category_in)
    return category


@router.post("/", response_model=schemas.Category)
def create(*, db: Session = Depends(db.get_db), category: schemas.CategoryCreate,) -> Any:
    """
    Create new Category.
    """
    if category.sequence is None:
        sequence = category_controller.get_max_sequence(db)
        category.sequence = sequence + 1

    try:
        item = category_controller.create(db=db, obj_in=category)
        return item
    except Exception as ex:
        raise HTTPException(status_code=404, detail=f"{ex}")


@router.delete("/{id}", response_model=schemas.Category)
def delete(*, db: Session = Depends(db.get_db), id: int) -> Any:
    """Delete category
    """
    try:
        category = category_controller.delete(db=db, id=id)
    except Exception as ex:
        raise HTTPException(status_code=404, detail=f"{ex}")
    return category
