from datetime import datetime
from enum import Enum
from typing import Protocol
from uuid import UUID, uuid4

from pydantic import Field

from enterprise_x.contracts.common import BaseContract, Severity, utc_now
from enterprise_x.integrations.erp.client import ERPClient
from enterprise_x.integrations.erp.schemas import Invoice, PurchaseOrder, Vendor


class FinancialAuditOutcome(str, Enum):
    CLEAR = "clear"
    REVIEW_REQUIRED = "review_required"


class FinancialFinding(BaseContract):
    code: str
    severity: Severity
    description: str
    evidence: list[str] = Field(min_length=1)


class FinancialAuditReport(BaseContract):
    audit_id: UUID = Field(default_factory=uuid4)
    invoice_id: str
    outcome: FinancialAuditOutcome
    findings: list[FinancialFinding] = Field(default_factory=list)
    audited_at: datetime = Field(default_factory=utc_now)


class FinancialSupervisor:
    async def audit_invoice(
        self, invoice_id: str, erp_client: ERPClient
    ) -> FinancialAuditReport:
        invoice = await erp_client.get_invoice(invoice_id)
        if invoice is None:
            raise LookupError(f"Invoice {invoice_id!r} was not found")
        if invoice.invoice_id != invoice_id:
            raise ValueError(
                f"ERP returned invoice {invoice.invoice_id!r} "
                f"for requested invoice {invoice_id!r}"
            )

        vendor = await erp_client.get_vendor(invoice.vendor_id)
        purchase_order = None
        if invoice.purchase_order_id is not None:
            purchase_order = await erp_client.get_purchase_order(
                invoice.purchase_order_id
            )

        findings = self._validate_invoice(invoice, vendor, purchase_order)
        outcome = (
            FinancialAuditOutcome.REVIEW_REQUIRED
            if findings
            else FinancialAuditOutcome.CLEAR
        )
        return FinancialAuditReport(
            invoice_id=invoice.invoice_id,
            outcome=outcome,
            findings=findings,
        )

    @staticmethod
    def _validate_invoice(
        invoice: Invoice,
        vendor: Vendor | None,
        purchase_order: PurchaseOrder | None,
    ) -> list[FinancialFinding]:
        findings: list[FinancialFinding] = []

        if vendor is None:
            findings.append(
                FinancialFinding(
                    code="vendor_not_found",
                    severity=Severity.HIGH,
                    description="The invoice references a vendor that was not found.",
                    evidence=[f"Invoice vendor ID: {invoice.vendor_id}"],
                )
            )
        else:
            if vendor.vendor_id != invoice.vendor_id:
                findings.append(
                    FinancialFinding(
                        code="vendor_id_mismatch",
                        severity=Severity.HIGH,
                        description="The ERP vendor record does not match the invoice vendor ID.",
                        evidence=[
                            f"Invoice vendor ID: {invoice.vendor_id}",
                            f"ERP vendor ID: {vendor.vendor_id}",
                        ],
                    )
                )
            if not vendor.active:
                findings.append(
                    FinancialFinding(
                        code="vendor_inactive",
                        severity=Severity.HIGH,
                        description="The invoice references an inactive vendor.",
                        evidence=[f"Vendor ID: {vendor.vendor_id}"],
                    )
                )

        if invoice.purchase_order_id is None:
            return findings

        if purchase_order is None:
            findings.append(
                FinancialFinding(
                    code="purchase_order_not_found",
                    severity=Severity.HIGH,
                    description="The invoice references a purchase order that was not found.",
                    evidence=[f"Purchase order ID: {invoice.purchase_order_id}"],
                )
            )
            return findings

        if purchase_order.purchase_order_id != invoice.purchase_order_id:
            findings.append(
                FinancialFinding(
                    code="purchase_order_id_mismatch",
                    severity=Severity.HIGH,
                    description="The ERP purchase order record does not match the invoice reference.",
                    evidence=[
                        f"Invoice purchase order ID: {invoice.purchase_order_id}",
                        f"ERP purchase order ID: {purchase_order.purchase_order_id}",
                    ],
                )
            )

        if invoice.vendor_id != purchase_order.vendor_id:
            findings.append(
                FinancialFinding(
                    code="purchase_order_vendor_mismatch",
                    severity=Severity.HIGH,
                    description="The invoice vendor does not match the purchase order vendor.",
                    evidence=[
                        f"Invoice vendor ID: {invoice.vendor_id}",
                        f"Purchase order vendor ID: {purchase_order.vendor_id}",
                    ],
                )
            )

        if invoice.currency != purchase_order.currency:
            findings.append(
                FinancialFinding(
                    code="currency_mismatch",
                    severity=Severity.HIGH,
                    description="The invoice currency does not match the purchase order currency.",
                    evidence=[
                        f"Invoice currency: {invoice.currency}",
                        f"Purchase order currency: {purchase_order.currency}",
                    ],
                )
            )

        if (
            invoice.currency == purchase_order.currency
            and invoice.total_amount > purchase_order.total_amount
        ):
            findings.append(
                FinancialFinding(
                    code="invoice_exceeds_purchase_order",
                    severity=Severity.HIGH,
                    description="The invoice total exceeds the purchase order total.",
                    evidence=[
                        f"Invoice total: {invoice.total_amount} {invoice.currency}",
                        (
                            "Purchase order total: "
                            f"{purchase_order.total_amount} {purchase_order.currency}"
                        ),
                    ],
                )
            )

        return findings