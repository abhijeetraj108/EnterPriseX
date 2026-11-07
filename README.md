enterprise-x/
│
├── README.md
├── pyproject.toml
├── uv.lock
├── .env
├── .env.example
├── .gitignore
├── compose.yaml
│
├── config/
│   ├── settings.py
│   ├── logging.yaml
│   └── policies.yaml
│
├── src/
│   └── enterprise_x/
│       │
│       ├── main.py
│       │
│       ├── api/
│       │   └── v1/
│       │       ├── router.py
│       │       ├── dependencies.py
│       │       └── endpoints/
│       │           ├── conversations.py
│       │           ├── investigations.py
│       │           ├── approvals.py
│       │           ├── actions.py
│       │           └── health.py
│       │
│       ├── application/
│       │   ├── conversation/
│       │   │   ├── manager.py
│       │   │   ├── intent_router.py
│       │   │   └── context_manager.py
│       │   │
│       │   ├── orchestration/
│       │   │   ├── graph.py
│       │   │   ├── state.py
│       │   │   ├── nodes/
│       │   │   └── routing/
│       │   │
│       │   └── investigation/
│       │       ├── service.py
│       │       └── planner.py
│       │
│       ├── contracts/
│       │   ├── common.py
│       │   ├── conversation.py
│       │   ├── investigation.py
│       │   ├── task.py
│       │   ├── evidence.py
│       │   ├── finding.py
│       │   ├── report.py
│       │   ├── approval.py
│       │   ├── action.py
│       │   └── events.py
│       │
│       ├── departments/
│       │   │
│       │   ├── financial/
│       │   │   ├── supervisor.py
│       │   │   ├── query/
│       │   │   ├── investigation/
│       │   │   ├── agents/
│       │   │   ├── tools/
│       │   │   └── workflows/
│       │   │
│       │   ├── cybersecurity/
│       │   │   ├── supervisor.py
│       │   │   ├── query/
│       │   │   ├── investigation/
│       │   │   ├── agents/
│       │   │   ├── tools/
│       │   │   └── workflows/
│       │   │
│       │   ├── supply_chain/
│       │   │   ├── supervisor.py
│       │   │   ├── query/
│       │   │   ├── investigation/
│       │   │   ├── agents/
│       │   │   ├── tools/
│       │   │   └── workflows/
│       │   │
│       │   ├── it_operations/
│       │   │   ├── supervisor.py
│       │   │   ├── query/
│       │   │   ├── investigation/
│       │   │   ├── agents/
│       │   │   ├── tools/
│       │   │   └── workflows/
│       │   │
│       │   └── software_delivery/
│       │       ├── supervisor.py
│       │       ├── query/
│       │       ├── investigation/
│       │       ├── agents/
│       │       ├── tools/
│       │       └── workflows/
│       │
│       ├── platform/
│       │   ├── evidence/
│       │   ├── approvals/
│       │   ├── actions/
│       │   ├── audit/
│       │   ├── knowledge/
│       │   │   ├── ingestion/
│       │   │   └── retrieval/
│       │   ├── authentication/
│       │   └── authorization/
│       │
│       ├── integrations/
│       │   ├── erp/
│       │   │   ├── client.py
│       │   │   └── schemas.py
│       │   ├── mcp/
│       │   └── external_systems/
│       │
│       ├── agents/
│       │   ├── base.py
│       │   ├── model_factory.py
│       │   ├── prompts/
│       │   └── tools/
│       │
│       └── infrastructure/
│           ├── database/
│           │   ├── connection.py
│           │   ├── models/
│           │   └── repositories/
│           │
│           ├── cache/
│           ├── messaging/
│           ├── vector_store/
│           ├── storage/
│           └── observability/
│
├── services/
│   └── erp_api/
│       ├── main.py
│       ├── routes/
│       ├── schemas/
│       └── services/
│
├── migrations/
│
├── evals/
│   ├── datasets/
│   ├── evaluators/
│   └── experiments/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── workflows/
│   └── e2e/
│
├── scripts/
│   ├── init_db.py
│   └── seed_data.py
│
└── storage/
    ├── documents/
    ├── evidence/
    └── reports/

# 1. EnterpriseX — Basic system architecture

My recommendation is to build EnterpriseX as a modular monolith initially, with a hierarchical multi-agent architecture inside it. This gives us clear departmental boundaries without the complexity of deploying five independent microservices from day one.

The architecture has six major layers:

```
                    EMPLOYEES / SYSTEM EVENTS
                              |
                              v
                 +--------------------------+
                 | API GATEWAY / FASTAPI    |
                 | Authentication & Access |
                 +--------------------------+
                              |
                              v
                 +--------------------------+
                 | CONVERSATION MANAGER     |
                 | Context, Intent, Routing |
                 +--------------------------+
                              |
                  +-----------+-----------+
                  |           |           |
                  v           v           v
              QUERY      INVESTIGATION   ACTION
                  |           |           |
                  |           v           |
                  |   +----------------+  |
                  |   | ENTERPRISE     |  |
                  |   | ORCHESTRATOR   |  |
                  |   +----------------+  |
                  |           |           |
                  |     +-----+-----+     |
                  |     |           |     |
                  |     v           v     |
                  |  FINANCIAL  CYBERSEC. |
                  |   AGENTS      AGENTS  |
                  |     |           |     |
                  |     +-----+-----+     |
                  |           |           |
                  |           v           |
                  |   EVIDENCE CORRELATION|
                  |   & RISK ASSESSMENT   |
                  |           |           |
                  +-----------+-----------+
                              |
                              v
                 +--------------------------+
                 | GOVERNANCE & ACTIONS     |
                 | Policy / Human Approval  |
                 | Execution / Verification |
                 +--------------------------+
                              |
                              v
                 +--------------------------+
                 | SHARED PLATFORM SERVICES |
                 |                            |
                 | PostgreSQL | Qdrant       |
                 | Redis      | Neo4j*       |
                 | Kafka*     | Object Store |
                 | Langfuse   | Audit        |
                 +--------------------------+
                              |
                              v
                            OUTPUT
```

\*Kafka and Neo4j are introduced when the requirements justify them; they are not mandatory in the first implementation.

## Why do we need different agents?

The point is not to create as many agents as possible. Each department handles a different business domain, uses different data sources, applies different rules and needs different expertise.

| Agent team                     | Why it is needed                                                                                      | Example responsibility                                                 |
| ------------------------------ | ----------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Financial Integrity            | Financial records require deterministic business validation and financial-domain expertise.           | Validate invoices, detect payment anomalies and verify vendors.        |
| Cybersecurity Intelligence     | Security investigation requires threat analysis, identity monitoring and incident-response knowledge. | Investigate suspicious logins, compromised accounts and attack chains. |
| Supply Chain Intelligence      | Procurement and supplier decisions require inventory, supplier and logistics analysis.                | Identify supplier risks and recommend alternative sourcing.            |
| IT Operations Intelligence     | Infrastructure problems require log analysis, telemetry and root-cause investigation.                 | Diagnose service outages and recommend recovery.                       |
| Software Delivery Intelligence | Software releases require code, testing and security analysis.                                        | Identify vulnerabilities and deployment risks.                         |

The central orchestrator is different from these agents. It does not replace their expertise. It decides which departments should participate, assigns work, coordinates dependencies and combines their results.

For example, if an employee account is compromised and a vendor's bank details are changed shortly afterwards:

- Cybersecurity investigates the employee account and login events.
- Financial Integrity investigates the vendor modification and related invoices.
- The orchestrator connects the evidence and assesses the combined risk.
- Governance controls whether a payment block or account restriction can be executed.

This is the reason to build a multi-agent system rather than one general-purpose agent.

# 2. Improved EnterpriseX problem statement

I've incorporated the architectural decisions we've discussed, particularly:

- Centralized conversation management with departmental intelligence.
- Hierarchical LangGraph orchestration and specialized subgraphs.
- Modular monolith first, with gradual service separation.
- Existing AI Invoice Auditor integration rather than rebuilding it.
- SentinelOps as the second department.
- PostgreSQL as the source of truth; Qdrant for semantic retrieval.
- Neo4j only when graph-based relationship analysis is justified.
- Separate read/investigation and knowledge-ingestion pipelines.
- Human approval, action verification and immutable audit history.
- Evaluation, observability, security and cost optimization as core engineering requirements.

The following is the revised version you can use as the master project specification.

# EnterpriseX — Project Problem Statement

## Agentic AI-Powered Enterprise Intelligence, Investigation & Decision-Orchestration Platform

## 1. Project Overview

EnterpriseX is an enterprise-grade, multi-agent AI platform designed to investigate complex business problems, monitor enterprise operations, correlate information across disconnected systems, and recommend or execute appropriate actions under controlled human supervision.

Modern enterprises operate across independent systems for finance, cybersecurity, supply chain, IT operations and software delivery. These systems generate large volumes of structured records, documents, alerts and operational events. However, critical business problems frequently span multiple departments.

Traditional systems generally investigate these problems independently, resulting in fragmented information, delayed investigations, duplicated effort and incomplete risk assessments.

EnterpriseX addresses this challenge through a coordinated network of specialized AI agents, a central Enterprise Orchestrator and a shared enterprise knowledge and evidence layer.

The platform should be capable of:

- Understanding natural-language requests from employees.
- Answering questions about enterprise information.
- Initiating independent or cross-department investigations.
- Dynamically planning and delegating tasks to specialized agents.
- Retrieving information from structured databases, APIs and enterprise knowledge sources.
- Sharing evidence and correlating findings across departments.
- Assessing combined business and operational risk.
- Generating evidence-backed recommendations.
- Requesting human authorization for sensitive actions.
- Executing permitted actions and verifying their outcomes.
- Maintaining traceable investigation history and audit records.

The objective is to build a reliable enterprise decision-support and action-orchestration system, not simply a chatbot with multiple agents.

---

## 2. Core Architectural Philosophy

EnterpriseX should follow these architectural principles:

1. **Centralized conversation management, decentralized departmental intelligence:** One conversation layer manages user interaction and context, while specialized departments own their domain-specific reasoning and workflows.
2. **Hierarchical multi-agent architecture:** A central Enterprise Orchestrator coordinates departmental supervisors, which manage their specialized agents and tools.
3. **Modular monolith first:** Start with clearly separated application modules and shared infrastructure. Introduce independently deployable services when justified by scalability, reliability or deployment requirements.
4. **Evidence-driven decisions:** Important findings and recommendations must be supported by traceable evidence and source references.
5. **Human-controlled execution:** Sensitive operations require authorization and policy enforcement. An LLM must never independently bypass approval controls.
6. **Source-of-truth data management:** PostgreSQL owns authoritative transactional records. Vector databases and graph representations are derived knowledge layers.
7. **Incremental development:** Start with Financial Integrity and Cybersecurity before expanding to other departments.

---

## 3. Core Departments and Specialized Agents

Each department must have its own supervisor, domain-specific workflows, tools, objectives and data access boundaries.

### A. Financial Integrity

**Purpose:** Investigate financial inconsistencies, fraudulent transactions and vendor-related risks.

Responsibilities:

- Invoice auditing and validation.
- Vendor verification and bank-account change monitoring.
- Purchase-order and goods-receipt validation.
- Payment fraud and anomaly detection.
- Financial discrepancy investigation.
- Financial risk assessment.

Specialized capabilities may include invoice validation agents, vendor verification agents, payment anomaly investigators and financial risk analysts.

**Existing implementation:** Integrate the existing AI Invoice Auditor as the foundation of this department. Preserve its validation logic, ERP interface, reporting functionality and audit history rather than rebuilding it unnecessarily.

### B. Cybersecurity Intelligence

**Purpose:** Investigate security alerts, identify potential compromises and understand attack relationships.

Responsibilities:

- Security alert investigation.
- Threat intelligence enrichment.
- Identity and access compromise detection.
- Suspicious login and endpoint analysis.
- Attack-chain reconstruction.
- Incident investigation and response recommendations.

Specialized capabilities may include alert investigation agents, identity analysis agents, threat intelligence agents and incident response planners.

**Planned implementation:** Develop SentinelOps as the cybersecurity department.

### C. Supply Chain Intelligence

**Purpose:** Identify supplier risks and support procurement and inventory decisions.

Responsibilities:

- Supplier risk monitoring.
- Inventory shortage prediction.
- Procurement analysis.
- Supplier dependency investigation.
- Alternative sourcing recommendations.
- Supply-chain disruption assessment.

### D. IT Operations Intelligence

**Purpose:** Investigate infrastructure and application failures and support operational recovery.

Responsibilities:

- Infrastructure monitoring.
- Log and telemetry analysis.
- Root-cause investigation.
- Service dependency analysis.
- Incident prioritization.
- Recovery recommendations and verification.

### E. Software Delivery Intelligence

**Purpose:** Improve software quality, release reliability and development security.

Responsibilities:

- Code review and analysis.
- Automated testing support.
- Vulnerability detection.
- Dependency and configuration risk analysis.
- Deployment risk assessment.
- Release recommendations and verification.

**Development priority:** Initially implement Financial Integrity and Cybersecurity. Introduce the remaining departments after the central architecture and cross-domain workflows are operational.

---

## 4. Central Enterprise Orchestrator

The Enterprise Orchestrator is responsible for coordinating investigations across departments.

It should not independently duplicate every department's expertise. Instead, it should understand the problem, plan the investigation, delegate work and combine departmental results.

Its responsibilities include:

1. Receive user requests, operational events and system alerts.
2. Understand investigation objectives and identify relevant entities.
3. Determine which departments should participate.
4. Create an investigation plan and standardized tasks.
5. Delegate tasks to departmental supervisors.
6. Support parallel execution when tasks are independent.
7. Manage dependencies between tasks.
8. Collect departmental findings and evidence.
9. Identify relationships between findings from different domains.
10. Detect conflicting, incomplete or unsupported conclusions.
11. Request additional investigation when necessary.
12. Assess combined enterprise risk and business impact.
13. Generate recommendations and response plans.
14. Coordinate approval and execution workflows.
15. Verify action outcomes and preserve the complete audit history.

The system must support both:

- Independent departmental investigations.
- Cross-domain investigations involving multiple departments.

---

## 5. Centralized Conversation Management

EnterpriseX must support natural-language interaction beyond explicitly initiated investigations.

Employees should be able to ask questions, request explanations, investigate problems, compare records and request permitted actions.

Examples:

- "Show invoice INV-801."
- "Why was this invoice rejected?"
- "Which vendors have recently changed their bank details?"
- "Investigate this suspicious employee login."
- "Check whether the vendor modification is connected to the employee's suspicious activity."
- "Recommend what action should be taken."

A centralized Conversation Manager should handle:

- Conversation creation and history.
- User and tenant context.
- Intent classification.
- Entity resolution.
- Follow-up question interpretation.
- Clarification when required.
- Department and workflow routing.
- Response synthesis.
- Conversation persistence.

Support at least four interaction paths:

1. Information queries.
2. Investigation requests.
3. Action requests.
4. Clarification requests.

Conversation history, active conversation context and enterprise knowledge must remain separate concepts.

The system should not pass the complete conversation history to every agent. Instead, it should provide relevant, permission-scoped context.

---

## 6. Hierarchical LangGraph Architecture

Use LangGraph to implement stateful, controllable and observable agent workflows.

Recommended workflow hierarchy:

### A. Main Conversation Graph

Handles:

- Loading conversation context.
- Intent and entity resolution.
- Conditional routing.
- Invoking query, investigation, action or clarification workflows.
- Synthesizing responses.
- Persisting conversation state.

### B. Enterprise Investigation Graph

Handles:

- Investigation creation.
- Investigation planning.
- Task generation.
- Department selection.
- Task dispatch.
- Parallel department execution.
- Report collection.
- Cross-domain correlation.
- Enterprise risk assessment.
- Unified report generation.

### C. Departmental Subgraphs

Each department has its own compiled LangGraph subgraph.

Departmental subgraphs contain:

- Department supervisor.
- Specialized agents.
- Domain-specific tools.
- Data retrieval and validation.
- Evidence collection.
- Finding generation.
- Department report generation.

### D. Governance and Action Graph

Handles:

- Action proposals.
- Policy and authorization checks.
- Human approval using LangGraph interrupts where appropriate.
- Action execution.
- Outcome verification.
- Audit persistence.

Use typed graph states, shared Pydantic contracts, conditional routing, fan-out/fan-in execution, checkpointing and controlled retries.

Do not create an unnecessarily large graph. Keep workflows modular and reusable.

---

## 7. Shared Enterprise Knowledge and Evidence Architecture

EnterpriseX should maintain a shared knowledge layer that allows departments to retrieve relevant historical information and learn from eligible, verified investigation outcomes.

However, RAG must not replace authoritative live database and API access.

### A. Investigation and Retrieval Pipeline

When an agent investigates a problem, it should:

1. Understand the investigation objective.
2. Identify relevant entities and data sources.
3. Retrieve relevant historical documents, reports, findings and policies.
4. Query live enterprise APIs and structured databases where current information is required.
5. Validate source relevance and access permissions.
6. Analyze the retrieved information.
7. Produce findings with evidence references and limitations.

### B. Knowledge Ingestion Pipeline

After an investigation or departmental workflow:

1. Persist authoritative findings and reports in PostgreSQL.
2. Record provenance, source references, timestamps and access policies.
3. Publish suitable events using an outbox-based event mechanism.
4. Process eligible knowledge asynchronously.
5. Generate embeddings for suitable documents and reports.
6. Store searchable vectors in Qdrant.
7. Maintain entity relationships in PostgreSQL initially.
8. Make eligible knowledge available to future investigations.

Not every database record should automatically become a RAG document.

Knowledge indexing must consider:

- Data sensitivity.
- Tenant boundaries.
- User permissions.
- Source reliability.
- Evidence provenance.
- Approval and decision status.
- Document lifecycle and retention policies.

Human-approved decisions must retain their context and must not become unquestionable universal facts.

PostgreSQL remains the source of truth. Derived vector and graph indexes should be rebuildable from authoritative records.

---

## 8. Data Storage and Database Architecture

Start with PostgreSQL as the primary transactional database.

Use logical schema ownership to isolate different domains.

Suggested initial schemas:

| Schema        | Ownership            | Example data                                      |
| ------------- | -------------------- | ------------------------------------------------- |
| platform      | Core platform        | Conversations, messages, investigations, tasks    |
| financial     | Financial department | Invoice audits, discrepancies, financial findings |
| cybersecurity | Security department  | Alerts, incidents, security findings              |
| erp           | ERP integration      | Vendors, purchase orders, PO lines, SKUs          |
| audit         | Cross-platform audit | Audit events, action history, approval history    |

The exact ownership of cross-cutting records should be finalized during database design.

### PostgreSQL

Use for:

- Transactional enterprise records.
- Conversations and investigation history.
- Tasks, evidence metadata and findings.
- Approvals and action records.
- ERP structured data.
- Audit trails and workflow persistence.

### Qdrant

Use for:

- Semantic document retrieval.
- Historical reports and eligible findings.
- Policies and operational documentation.
- Embedding-based knowledge search.

### Neo4j

Introduce when graph-based analysis has a demonstrated requirement, such as:

- Multi-hop entity relationship traversal.
- Fraud networks.
- Attack-chain reconstruction.
- Complex supplier dependency analysis.
- Large-scale relationship investigations.

Do not introduce Neo4j merely because the project uses Graph RAG. Start with PostgreSQL relationships and application-level correlation, then evaluate whether a graph database provides meaningful benefits.

### Redis

Use for:

- Caching frequently accessed data.
- Short-lived coordination state.
- Rate limiting.
- Temporary workflow support where appropriate.

### Object Storage

Store original documents, invoices, logs and large reports outside PostgreSQL.

The database should store references, paths, checksums and associated metadata rather than large binary files.

---

## 9. Event-Driven Architecture and Communication

Use a combination of communication mechanisms based on their purpose.

### REST APIs

Use FastAPI and versioned REST endpoints for:

- Client-to-backend communication.
- ERP integration.
- Synchronous service requests.
- Query and investigation operations.

### MCP

Use Model Context Protocol to expose controlled tools and resources to agents.

Examples:

- ERP vendor lookup.
- Purchase-order retrieval.
- Security alert retrieval.
- Investigation history retrieval.
- Approved action execution tools.

### A2A

Introduce Agent-to-Agent communication when departmental agents become independently deployed and need standardized service-to-service collaboration.

Do not require A2A for agents operating as internal subgraphs in the initial modular monolith.

### Kafka

Introduce Kafka for asynchronous events and workflows such as:

- Security alert ingestion.
- Investigation lifecycle events.
- Cross-department notifications.
- Knowledge indexing.
- Background processing.
- Monitoring and event-driven automation.

Use an outbox pattern to avoid inconsistencies between successful database transactions and event publication.

---

## 10. Human Approval and Action Governance

EnterpriseX must distinguish between recommending an action and executing it.

For every proposed operation:

1. Identify the requested action and target.
2. Validate user permissions and applicable policies.
3. Determine whether human approval is mandatory.
4. Present the action with supporting evidence and expected impact.
5. Obtain authorization when required.
6. Bind approval to the exact action, target and parameters.
7. Execute through an authorized integration.
8. Verify the actual outcome.
9. Record execution results and audit history.

Examples of sensitive actions:

- Blocking a vendor payment.
- Disabling a compromised employee account.
- Quarantining an endpoint.
- Changing procurement settings.
- Triggering a production deployment rollback.

Use idempotency keys, timeouts, retry policies and execution safeguards.

Approval cannot be bypassed by an LLM or a graph transition.

---

## 11. Core Technology Stack

| Area                | Technology                             |
| ------------------- | -------------------------------------- |
| Language            | Python                                 |
| Backend             | FastAPI                                |
| Data validation     | Pydantic v2                            |
| Agent framework     | LangChain                              |
| Agent orchestration | LangGraph                              |
| Agent communication | A2A, when independently deployed       |
| Tool integration    | MCP                                    |
| Primary database    | PostgreSQL                             |
| ORM and migrations  | SQLAlchemy 2.x, Alembic                |
| Vector database     | Qdrant                                 |
| Graph database      | Neo4j, when justified                  |
| Cache               | Redis                                  |
| Event streaming     | Kafka                                  |
| RAG                 | Hybrid retrieval, Graph RAG, reranking |
| Observability       | Langfuse                               |
| Testing             | Pytest and custom evaluation pipelines |
| Containerization    | Docker, Docker Compose                 |
| Frontend            | React and TypeScript                   |
| File storage        | Mounted or object storage              |

Technology should be introduced incrementally. Do not install every component during the foundation stage.

---

## 12. Engineering, Reliability and Security Requirements

The platform must prioritize:

### Architecture and maintainability

- Modular boundaries and clear ownership.
- Shared, versioned data contracts.
- Separation of API, application, domain and infrastructure layers.
- Independent deployment when justified.
- Consistent error handling and logging.

### Reliability

- Asynchronous and parallel execution.
- Timeouts and bounded retries.
- Idempotent operations.
- Persistent workflow checkpoints.
- Failure isolation between departments.
- Graceful handling of partial results.
- Background processing and recovery mechanisms.

### Performance and cost optimization

- Model selection based on task complexity.
- Avoid unnecessary agent-to-agent LLM calls.
- Cache repeated retrieval and deterministic results where safe.
- Limit prompt and conversation context.
- Use parallel execution for independent tasks.
- Monitor token usage, latency and cost per workflow.
- Use deterministic code for calculations and business rules.

### Security

- Authentication and role-based or attribute-based authorization.
- Tenant isolation.
- Least-privilege tool access.
- Prompt-injection protection.
- Treat retrieved documents and external tool results as untrusted input.
- Validate tool arguments and execution permissions.
- Protect credentials and sensitive data.
- Maintain immutable or append-only audit history where appropriate.

---

## 13. Evaluation and Observability

EnterpriseX must be evaluated using measurable outcomes rather than judging agents by whether their responses sound convincing.

Use Langfuse for tracing, prompt/version management, token and latency tracking, and evaluation support.

Develop custom evaluation datasets and evaluators for:

- Intent classification accuracy.
- Department selection and task-routing accuracy.
- Tool selection and tool-call accuracy.
- Task completion rate.
- Retrieval precision and recall.
- Retrieval relevance and factual grounding.
- Evidence attribution and citation accuracy.
- Finding correctness.
- Cross-agent collaboration quality.
- Investigation completeness.
- False-positive and false-negative rates.
- Recommendation quality.
- Approval and action-policy compliance.
- End-to-end investigation success.
- Cost and latency per investigation.

Use deterministic ground-truth checks wherever possible, supplemented by model-based evaluators and human review.

Evaluation should cover individual agents, subgraphs and complete end-to-end workflows.

---

## 14. Important End-to-End Demonstration Scenario

Demonstrate genuine cross-domain collaboration using the following scenario.

**Scenario: Possible Vendor Fraud Connected to Employee Account Compromise**

1. Cybersecurity detects a suspicious employee login.
2. The security department investigates the account and identifies potential compromise indicators.
3. A vendor bank-account modification is detected or reported.
4. Financial Integrity investigates the vendor's modification history, associated purchase orders and invoices.
5. A suspicious invoice associated with that vendor is identified.
6. The Enterprise Orchestrator recognizes shared entities and correlates the financial and cybersecurity evidence.
7. Both departments exchange relevant evidence and findings.
8. The orchestrator assesses combined business and security risk.
9. EnterpriseX generates a unified, evidence-backed investigation report.
10. The system proposes an appropriate response plan.
11. A human reviewer approves sensitive actions.
12. Authorized actions are executed through controlled integrations.
13. The system verifies action outcomes and records the complete investigation history.

The demonstration must prove that departments genuinely collaborate through shared evidence and investigation context, rather than simply generating separate summaries.

---

## 15. Incremental Development Roadmap

### Phase 1 — Platform Foundation

Establish:

- Overall architecture and module boundaries.
- Shared Pydantic contracts.
- PostgreSQL schema design and ownership.
- API communication standards.
- Environment configuration and Docker setup.
- FastAPI application foundation.
- Authentication and authorization foundations.
- Logging, error handling and testing conventions.

### Phase 2 — Financial Integrity

Integrate the existing AI Invoice Auditor.

Establish:

- Financial departmental supervisor.
- Invoice query and investigation workflows.
- ERP API integration.
- Vendor and PO validation.
- Financial findings and evidence contracts.
- Financial reports and audit persistence.

### Phase 3 — Cybersecurity Intelligence

Develop SentinelOps.

Establish:

- Security departmental supervisor.
- Security alert ingestion.
- Identity and suspicious-login investigation.
- Threat intelligence integration.
- Security findings and evidence.
- Incident reports and risk assessment.

### Phase 4 — Enterprise Orchestration

Implement:

- Central investigation planner.
- Department selection and task delegation.
- Parallel departmental execution.
- Cross-domain evidence sharing.
- Entity correlation.
- Combined enterprise risk assessment.
- Unified investigation reporting.

### Phase 5 — Shared Knowledge, Evaluation and Observability

Implement:

- Shared RAG retrieval.
- Knowledge ingestion pipeline.
- Hybrid search and reranking.
- Langfuse tracing and evaluation.
- Custom evaluation datasets.
- Performance and cost optimization.
- Knowledge access controls and provenance.

### Phase 6 — Supply Chain Intelligence

Introduce supplier risk, inventory and procurement investigations.

### Phase 7 — IT Operations and Software Delivery

Extend the platform to infrastructure diagnosis, service recovery, code analysis, testing and deployment risk.

---

## 16. Expected Final Outcome

The final deliverable should be a working enterprise-grade multi-agent platform capable of:

- Handling natural-language enterprise queries.
- Initiating and managing investigations.
- Coordinating specialized departmental agents.
- Sharing and correlating evidence across departments.
- Retrieving information from structured and unstructured enterprise sources.
- Producing explainable, evidence-backed findings.
- Recommending actions with business-impact awareness.
- Enforcing human approval and policy controls.
- Executing and verifying permitted operations.
- Maintaining complete investigation and audit history.
- Measuring agent quality, reliability, latency and cost.

The primary demonstration should be a working Financial Integrity + Cybersecurity system with genuine cross-domain investigation and controlled action execution.

The remaining departments should be added through the same shared contracts, governance model and orchestration architecture.

---

# Development Instruction

Act as a Principal Software Architect, Senior AI Engineer, Backend Engineer and Technical Mentor.

Help me design and implement EnterpriseX step by step using real-world software engineering and AI engineering practices.

Do not jump directly into implementation. First establish architecture, component responsibilities, data flow, shared contracts, database ownership, communication patterns and technical trade-offs.

For every major decision:

- Explain what it is.
- Explain why it is needed.
- Explain how it fits into EnterpriseX.
- Identify alternatives and trade-offs.
- Explain performance, reliability, security and cost implications.
- Explain how it can be tested and evaluated.

Follow these working principles:

1. Prioritize working functionality over unnecessary complexity.
2. Avoid creating agents when a deterministic function or ordinary service is sufficient.
3. Do not introduce infrastructure simply to use a particular technology.
4. Maintain clear boundaries between agents, APIs, databases and infrastructure.
5. Use shared, versioned Pydantic contracts for communication.
6. Keep authoritative business logic and sensitive operations outside uncontrolled LLM decisions.
7. Design for evidence provenance, auditability and human oversight.
8. Use evaluation and observability throughout development, not only at the end.
9. Provide understandable, file-by-file implementation guidance when coding begins.
10. Ensure every major architectural decision is defensible in Software Development Engineer and Agentic AI Engineer interviews.

Develop incrementally. Start with the foundation, integrate the existing Financial Integrity implementation, build Cybersecurity next, and then implement genuine enterprise-level orchestration and cross-domain collaboration.

## My final architectural recommendation

Three decisions are particularly important to preserve as we build:

1. Don't start with five independent microservices. Build the modular monolith and prove the architecture first.
2. Don't confuse RAG with live enterprise data access. Retrieve historical knowledge through RAG, but fetch current vendor, invoice and security status from authoritative APIs and databases.
3. Don't confuse agent collaboration with multiple agents chatting. Real collaboration means delegated tasks, shared evidence, correlated findings, explicit dependencies and measurable outcomes.

This revised specification should be the single reference document for the project going forward.&#x20;