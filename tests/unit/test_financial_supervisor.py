import asyncio
from decimal import Decimal

import pytest

from enterprise_x.contracts.common import Severity
from enterprise_x.departments.financial.supervisor import (
    FinancialAuditOutcome,
    FinancialSupervisor,
)
from enterprise_x.integrations.erp.schemas import Invoice, PurchaseOrder, Vendor


class FakeERPClient:
    def __init__(
        self,
        invoice: Invoice | None,
        vendor: Vendor | None,
        purchase_order: PurchaseOrder | None,
    ) -> None:
        self.invoice = invoice
        self.vendor = vendor
        self.purchase_order = purchase_order

    async def get_invoice(self, invoice_id: str) -> Invoice | None:
        return self.invoice

    async def get_vendor(self, vendor_id: str) -> Vendor | None:
        return self.vendor

    async def get_purchase_order(
        self, purchase_order_id: str
    ) -> PurchaseOrder | None:
        return self.purchase_order


def make_invoice(purchase_order_id: str | None = "PO-101") -> Invoice:
    return Invoice(
        invoice_id="INV-801",
        vendor_id="V-14",
        purchase_order_id=purchase_order_id,
        total_amount=Decimal("125.00"),
        currency="USD",
    )


def make_purchase_order(
    vendor_id: str = "V-14",
    total_amount: Decimal = Decimal("125.00"),
    currency: str = "USD",
) -> PurchaseOrder:
    return PurchaseOrder(
        purchase_order_id="PO-101",
        vendor_id=vendor_id,
        total_amount=total_amount,
        currency=currency,
    )
def test_audit_marks_matching_invoice_clear():
    supervisor = FinancialSupervisor()
    erp = FakeERPClient(
        make_invoice(),
        Vendor(vendor_id="V-14"),
        make_purchase_order(),
    )

    report = asyncio.run(supervisor.audit_invoice("INV-801", erp))

    assert report.outcome == FinancialAuditOutcome.CLEAR
    assert report.findings == []



def test_audit_reports_vendor_amount_and_currency_mismatches():
    supervisor = FinancialSupervisor()
    erp = FakeERPClient(
        make_invoice(),
        Vendor(vendor_id="V-14"),
        make_purchase_order(
            vendor_id="V-99",
            total_amount=Decimal("100.00"),
            currency="CAD",
        ),
    )

    report = asyncio.run(supervisor.audit_invoice("INV-801", erp))

    assert report.outcome == FinancialAuditOutcome.REVIEW_REQUIRED
    assert {finding.code for finding in report.findings} == {
        "purchase_order_vendor_mismatch",
        "currency_mismatch",
    }
    assert all(finding.severity == Severity.HIGH for finding in report.findings)


def test_audit_flags_invoice_amount_above_purchase_order():
    supervisor = FinancialSupervisor()
    erp = FakeERPClient(
        make_invoice(),
        Vendor(vendor_id="V-14"),
        make_purchase_order(total_amount=Decimal("100.00")),
    )

    report = asyncio.run(supervisor.audit_invoice("INV-801", erp))

    assert report.outcome == FinancialAuditOutcome.REVIEW_REQUIRED
    assert [finding.code for finding in report.findings] == [
        "invoice_exceeds_purchase_order"
    ]


def test_audit_allows_partial_invoice_below_purchase_order_total():
    supervisor = FinancialSupervisor()
    erp = FakeERPClient(
        make_invoice(),
        Vendor(vendor_id="V-14"),
        make_purchase_order(total_amount=Decimal("150.00")),
    )

    report = asyncio.run(supervisor.audit_invoice("INV-801", erp))

    assert report.outcome == FinancialAuditOutcome.CLEAR


def test_audit_flags_inactive_vendor_and_missing_purchase_order():
    supervisor = FinancialSupervisor()
    erp = FakeERPClient(
        make_invoice(),
        Vendor(vendor_id="V-14", active=False),
        None,
    )

    report = asyncio.run(supervisor.audit_invoice("INV-801", erp))

    assert report.outcome == FinancialAuditOutcome.REVIEW_REQUIRED
    assert {finding.code for finding in report.findings} == {
        "vendor_inactive",
        "purchase_order_not_found",
    }


def test_audit_flags_missing_vendor():
    supervisor = FinancialSupervisor()
    erp = FakeERPClient(
        make_invoice(purchase_order_id=None),
        None,
        None,
    )

    report = asyncio.run(supervisor.audit_invoice("INV-801", erp))

    assert report.outcome == FinancialAuditOutcome.REVIEW_REQUIRED
    assert [finding.code for finding in report.findings] == ["vendor_not_found"]


def test_audit_rejects_erp_response_for_different_invoice():
    supervisor = FinancialSupervisor()
    erp = FakeERPClient(
        make_invoice(),
        Vendor(vendor_id="V-14"),
        make_purchase_order(),
    )

    with pytest.raises(ValueError, match="requested invoice"):
        asyncio.run(supervisor.audit_invoice("INV-999", erp))


def test_audit_flags_erp_purchase_order_id_mismatch():
    supervisor = FinancialSupervisor()
    purchase_order = make_purchase_order()
    purchase_order.purchase_order_id = "PO-OTHER"
    erp = FakeERPClient(
        make_invoice(),
        Vendor(vendor_id="V-14"),
        purchase_order,
    )

    report = asyncio.run(supervisor.audit_invoice("INV-801", erp))

    assert "purchase_order_id_mismatch" in {
        finding.code for finding in report.findings
    }


def test_audit_raises_for_unknown_invoice():
    supervisor = FinancialSupervisor()
    erp = FakeERPClient(None, None, None)

    with pytest.raises(LookupError, match="INV-missing"):
        asyncio.run(supervisor.audit_invoice("INV-missing", erp))
def test_non_purchase_order_invoice_skips_purchase_order_lookup():
    supervisor = FinancialSupervisor()
    erp = FakeERPClient(
        make_invoice(purchase_order_id=None),
        Vendor(vendor_id="V-14"),
        None,
    )

    report = asyncio.run(supervisor.audit_invoice("INV-801", erp))

    assert report.outcome == FinancialAuditOutcome.CLEAR
