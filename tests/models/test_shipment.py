from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..helpers import create_valid_shipment


def test_shipment_create(dbsession: Session) -> None:
    shipment = create_valid_shipment()

    dbsession.add(shipment)
    dbsession.commit()
    dbsession.refresh(shipment)

    assert shipment.id is not None, "Id must be present"
    assert shipment.created_at is not None, "Created at was None, but should be set"
    assert shipment.updated_at is not None, "Updated at was None, but should be set"


def test_shipment_unique_name(dbsession: Session) -> None:
    shipment1 = create_valid_shipment()

    dbsession.add(shipment1)
    dbsession.commit()

    shipment2 = create_valid_shipment()
    dbsession.add(shipment2)
    try:
        dbsession.commit()
        assert False, "Shipment name must be unique"
    except IntegrityError:
        assert True, "Integrity Error expected"


def test_shipment_default_values(dbsession: Session) -> None:
    shipment = create_valid_shipment()
    dbsession.add(shipment)
    dbsession.commit()
    dbsession.refresh(shipment)

    assert shipment.id is not None, "Id must be present"
    assert shipment.days_to_deliver == 2, f"Default days to deliver should be 2 got {shipment.days_to_deliver}"
