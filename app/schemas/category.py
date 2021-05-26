from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BaseCategory(BaseModel):
    name: str
    description: Optional[str]
    sequence: Optional[int]
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class CategoryCreate(BaseCategory):
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CategoryUpdate(BaseCategory):
    id: int


class Category(CategoryCreate, CategoryUpdate):
    class Config:
        orm_mode = True
