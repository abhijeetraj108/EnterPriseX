# Financial invoice-audit core

This repository currently contains only the first implementation slice:
validating an invoice against its vendor and purchase order, using an ERP client
interface.

## What is included

- Typed invoice, vendor, and purchase-order schemas.
- An HTTP ERP adapter for fetching those records.
- Deterministic invoice/vendor/purchase-order audit rules and findings.
- Unit tests for audit outcomes and ERP HTTP behavior.

## Run the tests

```powershell
uv sync
uv run pytest -q
```

## Connect an ERP

Create an `httpx.AsyncClient`, configure the ERP base URL, then pass an
`ERPApiClient` to `FinancialSupervisor.audit_invoice`:

```python
import asyncio

import httpx

from enterprise_x.departments.financial.supervisor import FinancialSupervisor
from enterprise_x.integrations.erp.client import ERPApiClient


async def main() -> None:
    async with httpx.AsyncClient(timeout=10.0) as http_client:
        erp = ERPApiClient("https://your-erp.example/api/v1", http_client)
        report = await FinancialSupervisor().audit_invoice("INV-801", erp)
        print(report.model_dump_json(indent=2))


asyncio.run(main())
```

The adapter expects `GET /invoices/{invoice_id}`, `GET /vendors/{vendor_id}`,
and `GET /purchase-orders/{purchase_order_id}` under the configured base URL.
Responses must match the schemas in
[`src/enterprise_x/integrations/erp/schemas.py`](src/enterprise_x/integrations/erp/schemas.py).
HTTP 404 means the record was not found. Other HTTP errors and invalid response
bodies are raised instead of being silently treated as missing records.

## Audit behavior

- A missing invoice raises `LookupError`.
- Missing or inactive vendors and missing purchase orders require review.
- Vendor, purchase-order, and currency mismatches require review.
- An invoice above the purchase-order total in the same currency requires
  review. Lower totals are allowed for partial invoices.
- A matching invoice with no findings is marked clear.

This slice is a library, not a running API or a database-backed service.
Connecting a real ERP and adding persistence are later tasks. Cybersecurity,
orchestration, and RAG are intentionally not part of this implementation yet.
