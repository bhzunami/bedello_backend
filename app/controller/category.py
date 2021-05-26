import logging

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.controller.base_controller import BaseController
from app.models import Category
from app.schemas import CategoryCreate, CategoryUpdate

logger = logging.getLogger(__name__)


class CategoryController(BaseController[Category, CategoryCreate, CategoryUpdate]):
    def get_max_sequence(self, db: Session) -> int:
        max = db.query(func.max(Category.sequence)).scalar()
        logger.debug(f"Max category sequence {max}")
        return max


category_controller = CategoryController(Category)
