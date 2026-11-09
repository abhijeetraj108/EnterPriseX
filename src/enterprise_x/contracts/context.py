from uuid import UUID

from pydantic import Field

from enterprise_x.contracts.common import BaseContract


class EntityReference(BaseContract):
    entity_type: str
    entity_id: str
    description: str | None = None


class InvestigationContext(BaseContract):
    investigation_id: UUID
    tenant_id: UUID

    context_summary: str | None = None

    entities: list[EntityReference] = Field(
        default_factory=list
    )

    relevant_evidence_ids: list[UUID] = Field(
        default_factory=list
    )

    constraints: list[str] = Field(
        default_factory=list
    )