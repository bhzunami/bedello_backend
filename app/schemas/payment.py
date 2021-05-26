from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class BasePayment(BaseModel):
    name: str
    description: Optional[str]
    additional_costs: float = 0.0
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @validator("additional_costs")
    def additonal_costs_must_be_equal_or_greater_0(cls: "BasePayment", v: float) -> float:
        if v < 0.0:
            raise ValueError("must be greater or equal 0")
        return v


class PaymentCreate(BasePayment):
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PaymentUpdate(BasePayment):
    id: int


class Payment(PaymentCreate, PaymentUpdate):
    class Config:
        orm_mode = True
