from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import Field

from enterprise_x.contracts.common import (
    BaseContract,
    Department,
)
from enterprise_x.contracts.context import InvestigationContext


class TaskRequest(BaseContract):

    task_id: UUID = Field(default_factory=uuid4)

    investigation_id: UUID
    tenant_id: UUID

    department: Department

    task_type: str
    objective: str = Field(min_length=1)

    context: InvestigationContext | None = None

    priority: str = "medium"

    constraints: list[str] = Field(
        default_factory=list
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    deadline: datetime | None = None