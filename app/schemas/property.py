from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.property_item import PropertyItem


class BaseProperty(BaseModel):
    name: str
    description: Optional[str]
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    property_items: List[PropertyItem]


class PropertyCreate(BaseProperty):
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PropertyUpdate(BaseProperty):
    id: int


class Property(PropertyCreate, PropertyUpdate):
    class Config:
        orm_mode = True
