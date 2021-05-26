from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator

from app.schemas.line_item import LineItem


class OrderBase(BaseModel):
    state: str
    status: str
    total_price: float
    pay_date: Optional[datetime]
    notes: Optional[str]
    line_items: List[LineItem]
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @validator("total_price")
    def total_price_must_be_greater_0(cls: "OrderBase", v: float) -> float:
        if v <= 0.0:
            raise ValueError("must be greater 0")
        return v

    @validator("line_items")
    def at_least_one_line_item_must_exists(cls: "OrderBase", v: List[LineItem]) -> List[LineItem]:
        if len(v) == 0:
            raise ValueError("at least one line item must exists")
        return v


class OrderCreate(OrderBase):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    pf_payment_method: Optional[str]
    pf_acceptance: Optional[str]
    pf_status: Optional[str]
    pf_payid: Optional[str]
    pf_brand: Optional[str]
    ip_address: Optional[str]


class OrderUpdate(OrderBase):
    id: int
    distribution_number: Optional[str]
    delivery_date: Optional[datetime]
    reminder_date: Optional[datetime]


class Order(OrderCreate, OrderUpdate):
    class Config:
        orm_mode = True
