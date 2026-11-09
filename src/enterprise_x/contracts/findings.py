from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import Field

from enterprise_x.contracts.common import (
    BaseContract,
    Department,
    FindingSeverity,
)


class Finding(BaseContract):

    finding_id: UUID = Field(default_factory=uuid4)

    department: Department

    category: str
    title: str
    description: str

    severity: FindingSeverity

    confidence: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0
    )

    evidence_ids: list[UUID] = Field(
        default_factory=list
    )

    entity_ids: list[str] = Field(
        default_factory=list
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class Recommendation(BaseContract):

    recommendation_id: UUID = Field(default_factory=uuid4)

    action_type: str
    description: str

    target_entity: str | None = None

    risk_level: FindingSeverity = FindingSeverity.MEDIUM

    approval_required: bool = True