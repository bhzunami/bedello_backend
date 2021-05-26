from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..helpers import create_valid_payment


def test_payment_create(dbsession: Session) -> None:
    payment = create_valid_payment()

    dbsession.add(payment)
    dbsession.commit()
    dbsession.refresh(payment)

    assert payment.id is not None, "Id must be present"
    assert payment.created_at is not None, "Created at was None, but should be set"
    assert payment.updated_at is not None, "Updated at was None, but should be set"


def test_payment_unique_name(dbsession: Session) -> None:
    payment1 = create_valid_payment()

    dbsession.add(payment1)
    dbsession.commit()

    payment2 = create_valid_payment()
    dbsession.add(payment2)
    try:
        dbsession.commit()
        assert False, "payment name must be unique"
    except IntegrityError:
        assert True, "Integrity Error expected"
