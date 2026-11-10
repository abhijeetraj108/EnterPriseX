from collections.abc import Iterator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import Engine, select, text
from sqlalchemy.orm import Session, sessionmaker

from enterprise_x.database.models.erp import (
    ERPInvoice,
    ERPPurchaseOrder,
    ERPVendor,
)
from enterprise_x.integrations.erp.database import (
    engine,
    initialize_database,
)
from enterprise_x.integrations.erp.schemas import (
    Invoice,
    PurchaseOrder,
    Vendor,
)
from enterprise_x.integrations.erp.seed import seed_database


def create_app(
    database_engine: Engine = engine,
) -> FastAPI:
    if database_engine.dialect.name == "sqlite":
        database_engine = database_engine.execution_options(
            schema_translate_map={"erp": None}
        )
    session_factory = sessionmaker(
        bind=database_engine,
        autoflush=False,
        expire_on_commit=False,
    )

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> Iterator[None]:
        initialize_database(database_engine)
        seed_database(database_engine)
        yield

    app = FastAPI(
        title="EnterpriseX ERP Service",
        version="1.0.0",
        lifespan=lifespan,
    )

    def get_session() -> Iterator[Session]:
        with session_factory() as session:
            yield session

    DatabaseSession = Annotated[Session, Depends(get_session)]

    @app.get("/health")
    def health(session: DatabaseSession) -> dict[str, str]:
        session.execute(text("SELECT 1"))
        return {"status": "ok"}

    @app.get("/api/v1/invoices/{invoice_id}", response_model=Invoice)
    def get_invoice(invoice_id: str, session: DatabaseSession) -> Invoice:
        invoice = session.get(ERPInvoice, invoice_id)
        if invoice is None:
            raise HTTPException(status_code=404, detail="Invoice not found")
        return Invoice(
            invoice_id=invoice.invoice_id,
            vendor_id=invoice.vendor_id,
            purchase_order_id=invoice.purchase_order_id,
            total_amount=invoice.total_amount,
            currency=invoice.currency,
            status=invoice.status,
        )

    @app.get("/api/v1/vendors/{vendor_id}", response_model=Vendor)
    def get_vendor(vendor_id: str, session: DatabaseSession) -> Vendor:
        vendor = session.get(ERPVendor, vendor_id)
        if vendor is None:
            raise HTTPException(status_code=404, detail="Vendor not found")
        return Vendor(
            vendor_id=vendor.vendor_id,
            active=vendor.active,
            bank_account_changed_at=vendor.bank_account_changed_at,
        )

    @app.get(
        "/api/v1/purchase-orders/{purchase_order_id}",
        response_model=PurchaseOrder,
    )
    def get_purchase_order(
        purchase_order_id: str,
        session: DatabaseSession,
    ) -> PurchaseOrder:
        purchase_order = session.get(ERPPurchaseOrder, purchase_order_id)
        if purchase_order is None:
            raise HTTPException(
                status_code=404, detail="Purchase order not found"
            )
        return PurchaseOrder(
            purchase_order_id=purchase_order.purchase_order_id,
            vendor_id=purchase_order.vendor_id,
            total_amount=purchase_order.total_amount,
            currency=purchase_order.currency,
        )

    @app.get("/api/v1/invoices", response_model=list[Invoice])
    def list_invoices(session: DatabaseSession) -> list[Invoice]:
        invoices = session.scalars(
            select(ERPInvoice).order_by(ERPInvoice.invoice_id)
        )
        return [
            Invoice(
                invoice_id=invoice.invoice_id,
                vendor_id=invoice.vendor_id,
                purchase_order_id=invoice.purchase_order_id,
                total_amount=invoice.total_amount,
                currency=invoice.currency,
                status=invoice.status,
            )
            for invoice in invoices
        ]

    return app


app = create_app()
