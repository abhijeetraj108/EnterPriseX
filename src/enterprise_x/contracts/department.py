from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import Field

from enterprise_x.contracts.common import (
    BaseContract,
    Department,
    TaskStatus,
)
from enterprise_x.contracts.evidence import Evidence
from enterprise_x.contracts.findings import (
    Finding,
    Recommendation,
)


class DepartmentResponse(BaseContract):

    response_id: UUID = Field(default_factory=uuid4)

    task_id: UUID
    investigation_id: UUID
    tenant_id: UUID

    department: Department

    status: TaskStatus

    summary: str

    findings: list[Finding] = Field(
        default_factory=list
    )

    evidence: list[Evidence] = Field(
        default_factory=list
    )

    recommendations: list[Recommendation] = Field(
        default_factory=list
    )

    limitations: list[str] = Field(
        default_factory=list
    )

    unresolved_questions: list[str] = Field(
        default_factory=list
    )

    error_message: str | None = None

    completed_at: datetime | None = None