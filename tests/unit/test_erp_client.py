import asyncio
from decimal import Decimal
from typing import Callable

import httpx
import pytest
from pydantic import ValidationError

from enterprise_x.integrations.erp.client import ERPApiClient
from enterprise_x.integrations.erp.schemas import Invoice


def build_client(
    handler: Callable[[httpx.Request], httpx.Response],
) -> tuple[ERPApiClient, httpx.AsyncClient]:
    http_client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
    )
    return ERPApiClient("https://erp.example/api/v1/", http_client), http_client


def test_get_invoice_parses_erp_response_and_encodes_id():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.raw_path == b"/api/v1/invoices/INV%2F801"
        return httpx.Response(
            200,
            json={
                "invoice_id": "INV/801",
                "vendor_id": "V-14",
                "purchase_order_id": "PO-101",
                "total_amount": "125.00",
                "currency": "USD",
            },
        )

    api, http_client = build_client(handler)
    try:
        invoice = asyncio.run(api.get_invoice("INV/801"))
    finally:
        asyncio.run(http_client.aclose())

    assert invoice == Invoice(
        invoice_id="INV/801",
        vendor_id="V-14",
        purchase_order_id="PO-101",
        total_amount=Decimal("125.00"),
        currency="USD",
    )


def test_get_vendor_returns_none_for_404():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/vendors/V-missing"
        return httpx.Response(404)

    api, http_client = build_client(handler)
    try:
        vendor = asyncio.run(api.get_vendor("V-missing"))
    finally:
        asyncio.run(http_client.aclose())

    assert vendor is None


def test_get_purchase_order_raises_for_server_error():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/purchase-orders/PO-101"
        return httpx.Response(503)

    api, http_client = build_client(handler)
    try:
        with pytest.raises(httpx.HTTPStatusError):
            asyncio.run(api.get_purchase_order("PO-101"))
    finally:
        asyncio.run(http_client.aclose())


def test_get_invoice_surfaces_invalid_erp_payload():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"invoice_id": "INV-801"})

    api, http_client = build_client(handler)
    try:
        with pytest.raises(ValidationError):
            asyncio.run(api.get_invoice("INV-801"))
    finally:
        asyncio.run(http_client.aclose())
