from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import Field

from enterprise_x.contracts.common import BaseContract


class InvoiceStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    PAID = "paid"
    REJECTED = "rejected"


class Invoice(BaseContract):
    invoice_id: str = Field(min_length=1)
    vendor_id: str = Field(min_length=1)
    purchase_order_id: str | None = None
    total_amount: Decimal = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)
    status: InvoiceStatus = InvoiceStatus.SUBMITTED


class PurchaseOrder(BaseContract):
    purchase_order_id: str = Field(min_length=1)
    vendor_id: str = Field(min_length=1)
    total_amount: Decimal = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)


class Vendor(BaseContract):
    vendor_id: str = Field(min_length=1)
    active: bool = True
    bank_account_changed_at: datetime | None = None