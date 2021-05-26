from sqlalchemy.orm import Session

from app.models import LineItem, Order, Payment, Product, Shipment

from ..helpers import setup_store


def test_order_create(dbsession: Session) -> None:
    # Setup store
    setup_store(dbsession)
    hat = dbsession.query(Product).filter(Product.name == "Base cap").first()
    shirt1 = dbsession.query(Product).filter(Product.name == "Shirt 1").first()
    shirt2 = dbsession.query(Product).filter(Product.name == "Shirt 2").first()
    line_item1 = LineItem(product=hat, quantity=2)
    line_item2 = LineItem(product=shirt1, quantity=5)
    line_item3 = LineItem(product=shirt2, quantity=1)

    shipment = dbsession.query(Shipment).filter(Shipment.name == "Mail").first()
    payment = dbsession.query(Payment).filter(Payment.name == "Credit_Card").first()
    order = Order(line_items=[line_item1, line_item2, line_item3], shipment=shipment, payment=payment, total_price=300)

    dbsession.add(order)
    dbsession.commit()
    dbsession.refresh(order)

    assert order.id is not None, "Id must be present, was None"
    assert len(order.line_items) == 3, f"Expected 3 line items got {len(order.line_items)}"
    assert (
        order.line_items[0].product.name == hat.name
    ), f"Expected name {hat.name} got {order.line_items[0].product.name}"

    assert order.line_items[0].order.id == order.id, f"Expected id {order.id} got {order.line_items[0].order.id}"
    assert order.shipment.name == shipment.name, f"Expected {shipment.name} got {order.shipment.name}"
