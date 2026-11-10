from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from enterprise_x.database.base import Base, TimestampMixin


class ERPVendor(Base, TimestampMixin):
    __tablename__ = "vendors"
    __table_args__ = {"schema": "erp"}

    vendor_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    bank_account_changed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class ERPPurchaseOrder(Base, TimestampMixin):
    __tablename__ = "purchase_orders"
    __table_args__ = {"schema": "erp"}

    purchase_order_id: Mapped[str] = mapped_column(
        String(100), primary_key=True
    )
    vendor_id: Mapped[str] = mapped_column(
        String(100),
        ForeignKey("erp.vendors.vendor_id"),
        nullable=False,
    )
    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False
    )
    currency: Mapped[str] = mapped_column(String(3), nullable=False)


class ERPInvoice(Base, TimestampMixin):
    __tablename__ = "invoices"
    __table_args__ = {"schema": "erp"}

    invoice_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    vendor_id: Mapped[str] = mapped_column(
        String(100),
        ForeignKey("erp.vendors.vendor_id"),
        nullable=False,
    )
    purchase_order_id: Mapped[str | None] = mapped_column(
        String(100),
        ForeignKey("erp.purchase_orders.purchase_order_id"),
        nullable=True,
    )
    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False
    )
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    status: Mapped[str] = mapped_column(
        String(40), default="submitted", nullable=False
    )

    vendor: Mapped[ERPVendor] = relationship()
    purchase_order: Mapped[ERPPurchaseOrder | None] = relationship()
