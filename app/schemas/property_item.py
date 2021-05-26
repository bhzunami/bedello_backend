from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BasePropertyItem(BaseModel):
    name: str
    description: Optional[str]
    item_order: int
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class PropertyItemCreate(BasePropertyItem):
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PropertyItemUpdate(BasePropertyItem):
    id: int


class PropertyItem(PropertyItemCreate, PropertyItemUpdate):
    class Config:
        orm_mode = True
