from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class BaseShipment(BaseModel):
    name: str
    description: Optional[str]
    additional_costs: float = 0.0
    days_to_deliver: int
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @validator("additional_costs")
    def additonal_costs_must_be_equal_or_greater_0(cls: "BaseShipment", v: float) -> float:
        if v < 0.0:
            raise ValueError("must be greater or equal 0")
        return v

    @validator("days_to_deliver")
    def days_to_deliver_must_be_greater_0(cls: "BaseShipment", v: int) -> int:
        if v <= 0:
            raise ValueError("must be greater 0")
        return v


class ShipmentCreate(BaseShipment):
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ShipmentUpdate(BaseShipment):
    id: int


class Shipment(ShipmentCreate, ShipmentUpdate):
    class Config:
        orm_mode = True
