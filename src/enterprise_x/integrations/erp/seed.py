import json
from pathlib import Path

from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from enterprise_x.database.models.erp import (
    ERPInvoice,
    ERPPurchaseOrder,
    ERPVendor,
)
from enterprise_x.integrations.erp.schemas import (
    Invoice,
    PurchaseOrder,
    Vendor,
)


def seed_database(database_engine: Engine) -> None:
    seed_path = Path(__file__).with_name("seed_data.json")
    with seed_path.open(encoding="utf-8") as seed_file:
        seed_data = json.load(seed_file)

    with sessionmaker(bind=database_engine)() as session:
        _seed_vendors(session, seed_data["vendors"])
        session.flush()
        _seed_purchase_orders(session, seed_data["purchase_orders"])
        session.flush()
        _seed_invoices(session, seed_data["invoices"])
        session.commit()


def _seed_vendors(session: Session, records: list[dict[str, object]]) -> None:
    for record in records:
        vendor = Vendor.model_validate(record)
        if session.get(ERPVendor, vendor.vendor_id) is None:
            session.add(
                ERPVendor(
                    vendor_id=vendor.vendor_id,
                    active=vendor.active,
                    bank_account_changed_at=vendor.bank_account_changed_at,
                )
            )


def _seed_purchase_orders(
    session: Session, records: list[dict[str, object]]
) -> None:
    for record in records:
        purchase_order = PurchaseOrder.model_validate(record)
        if (
            session.get(ERPPurchaseOrder, purchase_order.purchase_order_id)
            is None
        ):
            session.add(
                ERPPurchaseOrder(
                    purchase_order_id=purchase_order.purchase_order_id,
                    vendor_id=purchase_order.vendor_id,
                    total_amount=purchase_order.total_amount,
                    currency=purchase_order.currency,
                )
            )


def _seed_invoices(session: Session, records: list[dict[str, object]]) -> None:
    for record in records:
        invoice = Invoice.model_validate(record)
        if session.get(ERPInvoice, invoice.invoice_id) is None:
            session.add(
                ERPInvoice(
                    invoice_id=invoice.invoice_id,
                    vendor_id=invoice.vendor_id,
                    purchase_order_id=invoice.purchase_order_id,
                    total_amount=invoice.total_amount,
                    currency=invoice.currency,
                    status=invoice.status.value,
                )
            )
