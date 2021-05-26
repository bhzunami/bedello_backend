from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator

from app.schemas.property import Property


class BaseProduct(BaseModel):
    name: str
    description: Optional[str]
    number: int
    price: float
    active_from: datetime = Field(default_factory=datetime.utcnow)
    active_until: Optional[datetime]
    sale_price: Optional[float]
    sale_from: Optional[datetime]
    sale_until: Optional[datetime]
    num_in_stock: int
    category_id: int
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @validator("number")
    def price_gt_eq_0(cls: "BaseProduct", v: int) -> int:
        if v < 0:
            raise ValueError("must be >= 0")
        return v

    @validator("price")
    def price_gt_0(cls: "BaseProduct", v: float) -> float:
        if v <= 0.0:
            raise ValueError("must be > 0")
        return v

    @validator("num_in_stock")
    def num_in_stock_gt_eq_0(cls: "BaseProduct", v: int) -> int:
        if v < 0:
            raise ValueError("must be >= 0")
        return v


class ProductCreate(BaseProduct):
    properties: Optional[List[Property]]
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ProductUpdate(BaseProduct):
    id: int
    properties: Optional[List[Property]]


class Product(ProductCreate, ProductUpdate):
    product_property: Optional[List[int]]

    class Config:
        orm_mode = True
