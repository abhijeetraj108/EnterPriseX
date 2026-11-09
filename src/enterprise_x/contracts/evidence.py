from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import Field

from enterprise_x.contracts.common import (
    BaseContract,
    EvidenceType,
)


class Evidence(BaseContract):

    evidence_id: UUID = Field(default_factory=uuid4)

    evidence_type: EvidenceType

    source_system: str
    source_reference: str

    description: str

    content_ref: str | None = None
    checksum: str | None = None

    collected_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    observed_at: datetime | None = None

    metadata: dict[str, str | int | float | bool | None] = Field(
        default_factory=dict
    )