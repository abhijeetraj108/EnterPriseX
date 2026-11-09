### Folder Structure
enterprise-x/
│
├── shared/
│   ├── contracts/
│   ├── config/
│   ├── database/
│   └── common/
│
├── departments/
│   │
│   ├── financial/
│   │   ├── agents/
│   │   ├── workflows/
│   │   ├── services/
│   │   ├── api/
│   │   ├── repositories/
│   │   └── tests/
│   │
│   └── cybersecurity/
│       ├── agents/
│       ├── workflows/
│       ├── services/
│       ├── api/
│       ├── repositories/
│       └── tests/
│
├── orchestrator/          # Phase 3
│   ├── agents/
│   ├── workflows/
│   ├── a2a/
│   └── tests/
│
├── knowledge/             # Phase 4
│   ├── ingestion/
│   ├── retrieval/
│   ├── embeddings/
│   └── tests/
│
├── infrastructure/
│   ├── docker/
│   └── logging/
│
├── migrations/
├── evals/
├── scripts/
├── pyproject.toml
├── .env.example
├── compose.yaml
└── README.md

## Phase 1
              FINANCIAL INTEGRITY
                       |
                       v
              Financial Supervisor
                       |
             +---------+----------+
             |                    |
             v                    v
       Invoice Query        Invoice Audit
             |                    |
             v                    v
       Retrieve Invoice     Document Processing
             |                    |
             v                    v
       ERP API Lookup       Internal Validation
             |                    |
             |                    v
             |              Business Validation
             |                    |
             +---------+----------+
                       |
                       v
                Findings & Evidence
                       |
                       v
                Financial Report
                       |
                       v
                 PostgreSQL

## Phase 2
            CYBERSECURITY INTELLIGENCE
                       |
                       v
              Security Supervisor
                       |
          +------------+------------+
          |            |            |
          v            v            v
      Alert Agent  Identity Agent  Threat Agent
          |            |            |
          v            v            v
      Log Analysis  Login Analysis  Threat Intel
          |            |            |
          +------------+------------+
                       |
                       v
               Evidence Collection
                       |
                       v
                Security Findings
                       |
                       v
                Incident Report
                       |
                       v
                   PostgreSQL
                  
## Phase 3
                   USER / EVENT
                        |
                        v
              +-------------------+
              | ENTERPRISE        |
              | ORCHESTRATOR      |
              +-------------------+
                        |
                        v
              Investigation Planner
                        |
                        v
                Department Selection
                        |
              +---------+---------+
              |                   |
              v                   v
       A2A Financial Agent   A2A Security Agent
              |                   |
              v                   v
       Financial Service    Security Service
              |                   |
              v                   v
       Financial Report     Security Report
              |                   |
              +---------+---------+
                        |
                        v
              Cross-Domain Correlation
                        |
                        v
               Enterprise Risk Analysis
                        |
                        v
               Unified Investigation Report
                        |
                        v
                       END

## Phase 4
          FINANCIAL FINDINGS       SECURITY FINDINGS
                  |                       |
                  +-----------+-----------+
                              |
                              v
                    Persist in PostgreSQL
                              |
                              v
                       Event / Outbox
                              |
                              v
                     Knowledge Processing
                              |
                   +----------+----------+
                   |                     |
                   v                     v
              Chunking              Entity Extraction
                   |                     |
                   v                     v
              Embeddings          Relationship Data
                   |                     |
                   v                     v
                Qdrant          PostgreSQL / Neo4j*
                   |                     |
                   +----------+----------+
                              |
                              v
                     SHARED KNOWLEDGE
                              |
                              v
                    Future Investigations

# Financial invoice-audit core

This repository currently contains only the first implementation slice:
validating an invoice against its vendor and purchase order, using an ERP client
interface.

## What is included

- Typed invoice, vendor, and purchase-order schemas.
- An HTTP ERP adapter for fetching those records.
- An MCP server that exposes ERP invoices, vendors, and purchase orders as
  read-only resource templates, plus an MCP adapter for the audit workflow.
- Deterministic invoice/vendor/purchase-order audit rules and findings.
- Unit tests for audit outcomes, ERP HTTP behavior, and MCP resource access.

## Run the tests

```powershell
uv sync
uv run pytest -q
```

## Run the ERP MCP server

The MCP server exposes these read-only resource templates:

- `erp://invoices/{invoice_id}`
- `erp://vendors/{vendor_id}`
- `erp://purchase-orders/{purchase_order_id}`

The server reads through the existing ERP HTTP adapter, so the ERP remains the
source of truth. Configure the adapter's base URL and start the stdio server:

```powershell
$env:ERP_API_BASE_URL = "https://your-erp.example/api/v1"
uv run enterprise-x-erp-mcp-server
```

Connect an MCP host to that command. For example, an MCP client can use the
same resource interface and pass it to the financial supervisor:

```python
import asyncio
from mcp import Client, StdioServerParameters

from enterprise_x.departments.financial.supervisor import FinancialSupervisor
from enterprise_x.integrations.erp.mcp_client import MCPResourceERPClient


async def main() -> None:
    server = StdioServerParameters(
        command="uv",
        args=["run", "enterprise-x-erp-mcp-server"],
        env={"ERP_API_BASE_URL": "https://your-erp.example/api/v1"},
    )
    async with Client(server) as mcp_client:
        erp = MCPResourceERPClient(mcp_client)
        report = await FinancialSupervisor().audit_invoice("INV-801", erp)
        print(report.model_dump_json(indent=2))


asyncio.run(main())
```

For consumers that do not need MCP, the `ERPApiClient` remains available for
direct use. The MCP client reports missing records as `null`; transport errors,
invalid JSON, and schema validation errors are surfaced to the caller.

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
