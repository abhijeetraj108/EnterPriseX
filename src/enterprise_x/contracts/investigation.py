from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import Field

from enterprise_x.contracts.common import (
    BaseContract,
    RiskLevel,
    utc_now,
)


class InvestigationStatus(str, Enum):
    CREATED = "created"
    PLANNING = "planning"
    INVESTIGATING = "investigating"
    CORRELATING = "correlating"
    RECOMMENDATION_READY = "recommendation_ready"
    AWAITING_APPROVAL = "awaiting_approval"
    EXECUTING = "executing"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


class InvestigationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Department(str, Enum):
    FINANCIAL = "financial"
    CYBERSECURITY = "cybersecurity"
    SUPPLY_CHAIN = "supply_chain"
    IT_OPERATIONS = "it_operations"
    SOFTWARE_DELIVERY = "software_delivery"


class Investigation(BaseContract):
    investigation_id: UUID = Field(default_factory=uuid4)

    tenant_id: UUID
    requested_by: UUID

    title: str
    description: str

    status: InvestigationStatus = InvestigationStatus.CREATED
    priority: InvestigationPriority = InvestigationPriority.MEDIUM
    risk_level: RiskLevel = RiskLevel.LOW

    departments: list[Department] = Field(default_factory=list)
    objectives: list[str] = Field(default_factory=list)

    parent_investigation_id: UUID | None = None

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)