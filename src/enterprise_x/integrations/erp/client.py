from typing import Protocol, TypeVar
from urllib.parse import quote

import httpx

from enterprise_x.integrations.erp.schemas import Invoice, PurchaseOrder, Vendor

ERPModel = TypeVar("ERPModel", Invoice, PurchaseOrder, Vendor)


class ERPClient(Protocol):
    async def get_invoice(self, invoice_id: str) -> Invoice | None: ...

    async def get_vendor(self, vendor_id: str) -> Vendor | None: ...

    async def get_purchase_order(
        self, purchase_order_id: str
    ) -> PurchaseOrder | None: ...


class ERPApiClient:
    def __init__(self, base_url: str, client: httpx.AsyncClient) -> None:
        self._base_url = base_url.rstrip("/")
        self._client = client

    async def get_invoice(self, invoice_id: str) -> Invoice | None:
        return await self._get(
            f"invoices/{quote(invoice_id, safe='')}", Invoice
        )

    async def get_vendor(self, vendor_id: str) -> Vendor | None:
        return await self._get(f"vendors/{quote(vendor_id, safe='')}", Vendor)

    async def get_purchase_order(
        self, purchase_order_id: str
    ) -> PurchaseOrder | None:
        return await self._get(
            f"purchase-orders/{quote(purchase_order_id, safe='')}",
            PurchaseOrder,
        )

    async def _get(
        self, path: str, model_type: type[ERPModel]
    ) -> ERPModel | None:
        response = await self._client.get(f"{self._base_url}/{path}")
        if response.status_code == httpx.codes.NOT_FOUND:
            return None
        response.raise_for_status()
        return model_type.model_validate(response.json())
