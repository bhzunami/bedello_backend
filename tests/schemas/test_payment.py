from typing import Any, Dict

import pytest  # type: ignore
from pydantic import ValidationError

from app.schemas import Payment, PaymentCreate, PaymentUpdate


@pytest.mark.parametrize("additional_costs", [0.0, 1000.55])
def test_payment_create(additional_costs: float) -> None:
    props: Dict[str, Any] = {
        "name": "payment Test",
        "additional_costs": additional_costs,
        "updated_at": "2020-08-15T14:33:30.625578",
        "created_at": "2020-08-15T14:33:30.625578",
    }

    payment: PaymentCreate = PaymentCreate(**props)
    assert payment is not None, "Should be valid payment"


@pytest.mark.parametrize("additional_costs", [-1.0, -0.1])
def test_payment_create_with_additonal_costs(additional_costs: int) -> None:
    props: Dict[str, Any] = {
        "name": "payment Test",
        "additional_costs": additional_costs,
        "updated_at": "2020-08-15T14:33:30.625578",
        "created_at": "2020-08-15T14:33:30.625578",
    }

    try:
        PaymentCreate(**props)
        assert False, "Additonal costs can not be less than 0"
    except ValidationError as ex:
        assert ex.errors() == [
            {"loc": ("additional_costs",), "msg": "must be greater or equal 0", "type": "value_error"}
        ]


def test_payment_create_default_values() -> None:
    props: Dict[str, Any] = {
        "name": "Payment Test",
    }

    payment: PaymentCreate = PaymentCreate(**props)
    assert payment.additional_costs == 0.0, "Default value should be 0.0"
    assert payment.created_at is not None, "Created at should be filled out"
    assert payment.updated_at is not None, "Updated at should be filled out"


def test_payment_update() -> None:
    props: Dict[str, Any] = {
        "id": 45,
        "name": "Payment Test",
    }
    payment: PaymentUpdate = PaymentUpdate(**props)
    assert payment.additional_costs == 0.0, "Default value should be 0.0"
    assert payment.updated_at is not None, "Updated at should be filled out"


def test_payment_orm() -> None:
    props: Dict[str, Any] = {
        "id": 45,
        "name": "payment Test",
        "days_to_deliver": 1,
    }
    payment: Payment = Payment(**props)
    assert payment.additional_costs == 0.0, "Default value should be 0.0"
    assert payment.created_at is not None, "Created at should be filled out"
    assert payment.updated_at is not None, "Updated at should be filled out"
