from datetime import datetime

from pydantic import BaseModel, Field, validator


class LineItemBase(BaseModel):
    product_id: int
    quantity: int
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @validator("quantity")
    def quanity_must_be_greater_0(cls: "LineItemBase", v: int) -> int:
        if v <= 0:
            raise ValueError("must be greater 0")
        return v


class LineItemCreate(LineItemBase):
    created_at: datetime = Field(default_factory=datetime.utcnow)


class LineItemUpdate(LineItemBase):
    id: int


class LineItem(LineItemCreate, LineItemUpdate):
    class Config:
        orm_mode = True
