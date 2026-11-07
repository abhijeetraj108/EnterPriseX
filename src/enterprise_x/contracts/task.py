from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import Field

from enterprise_x.contracts.common import BaseContract, utc_now
from enterprise_x.contracts.investigation import (
    Department,
    InvestigationPriority,
)


class TaskStatus(str, Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class TaskType(str, Enum):
    INFORMATION_RETRIEVAL = "information_retrieval"
    DATA_VALIDATION = "data_validation"
    RISK_ASSESSMENT = "risk_assessment"
    SECURITY_ANALYSIS = "security_analysis"
    EVIDENCE_COLLECTION = "evidence_collection"
    INVESTIGATION = "investigation"


class InvestigationTask(BaseContract):
    task_id: UUID = Field(default_factory=uuid4)

    investigation_id: UUID

    assigned_department: Department
    assigned_agent: str | None = None

    task_type: TaskType
    objective: str

    input_context: dict = Field(default_factory=dict)
    constraints: list[str] = Field(default_factory=list)

    priority: InvestigationPriority = InvestigationPriority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING

    created_at: datetime = Field(default_factory=utc_now)
    deadline: datetime | None = None
    result_ref: str | None = None