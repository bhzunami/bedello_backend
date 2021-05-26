from typing import Any, Dict

import pytest  # type: ignore
from pydantic import ValidationError

from app.schemas import Product, ProductCreate, ProductUpdate


def test_product_create() -> None:
    props: Dict[str, Any] = {
        "name": "Shipment Test",
        "additional_costs": 2.5,
        "days_to_deliver": 2,
        "num_in_stock": 100,
        "updated_at": "2020-08-15T14:33:30.625578",
        "created_at": "2020-08-15T14:33:30.625578",
    }

    # product: ProductCreate = ProductCreate(**props)
    # assert product is not None, "Should be valid product"
