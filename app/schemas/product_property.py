from pydantic import BaseModel


class BaseProductProperty(BaseModel):
    product_id: int
    property_id: int


class ProductPropertyCreate(BaseProductProperty):
    pass


class ProductPropertyUpdate(BaseProductProperty):
    pass


class ProductProperty(ProductPropertyCreate):
    class Config:
        orm_mode = True
