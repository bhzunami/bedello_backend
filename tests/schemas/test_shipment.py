from typing import Any, Dict

import pytest  # type: ignore
from pydantic import ValidationError

from app.schemas import Shipment, ShipmentCreate, ShipmentUpdate


def test_shipment_create() -> None:
    props: Dict[str, Any] = {
        "name": "Shipment Test",
        "additional_costs": 2.5,
        "days_to_deliver": 2,
        "updated_at": "2020-08-15T14:33:30.625578",
        "created_at": "2020-08-15T14:33:30.625578",
    }

    shipment: ShipmentCreate = ShipmentCreate(**props)
    assert shipment is not None, "Should be valid shipment"


@pytest.mark.parametrize("days_to_teliver", [0, -12])
def test_shipment_create_with_negative_days_to_deliver(days_to_teliver: int) -> None:
    props: Dict[str, Any] = {
        "name": "Shipment Test",
        "additional_costs": 2.5,
        "days_to_deliver": days_to_teliver,
        "updated_at": "2020-08-15T14:33:30.625578",
        "created_at": "2020-08-15T14:33:30.625578",
    }

    try:
        ShipmentCreate(**props)
        assert False, "Negative days to deliver are not allowed"
    except ValidationError as ex:
        assert ex.errors() == [{"loc": ("days_to_deliver",), "msg": "must be greater 0", "type": "value_error"}]


@pytest.mark.parametrize("additional_costs", [-1.0, -0.1])
def test_shipment_create_with_additonal_costs(additional_costs: int) -> None:
    props: Dict[str, Any] = {
        "name": "Shipment Test",
        "additional_costs": additional_costs,
        "days_to_deliver": 1,
        "updated_at": "2020-08-15T14:33:30.625578",
        "created_at": "2020-08-15T14:33:30.625578",
    }

    try:
        ShipmentCreate(**props)
        assert False, "Additonal costs can not be less than 0"
    except ValidationError as ex:
        assert ex.errors() == [
            {"loc": ("additional_costs",), "msg": "must be greater or equal 0", "type": "value_error"}
        ]


def test_shipment_create_default_values() -> None:
    props: Dict[str, Any] = {
        "name": "Shipment Test",
        "days_to_deliver": 1,
    }

    shipment: ShipmentCreate = ShipmentCreate(**props)
    assert shipment.additional_costs == 0.0, "Default value should be 0.0"
    assert shipment.created_at is not None, "Created at should be filled out"
    assert shipment.updated_at is not None, "Updated at should be filled out"


def test_shipment_update() -> None:
    props: Dict[str, Any] = {
        "id": 45,
        "name": "Shipment Test",
        "days_to_deliver": 1,
    }
    shipment: ShipmentUpdate = ShipmentUpdate(**props)
    assert shipment.updated_at is not None, "Updated at should be filled out"


def test_shipment_orm() -> None:
    props: Dict[str, Any] = {
        "id": 45,
        "name": "Shipment Test",
        "days_to_deliver": 1,
    }
    shipment: Shipment = Shipment(**props)
    assert shipment.additional_costs == 0.0, "Default value should be 0.0"
    assert shipment.created_at is not None, "Created at should be filled out"
    assert shipment.updated_at is not None, "Updated at should be filled out"
