from datetime import datetime
from uuid import UUID, uuid4

from pydantic import Field

from enterprise_x.contracts.common import (
    BaseContract,
    EntityReference,
    utc_now,
)


class Conversation(BaseContract):
    conversation_id: UUID = Field(default_factory=uuid4)

    user_id: UUID
    tenant_id: UUID

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class ConversationMessage(BaseContract):
    message_id: UUID = Field(default_factory=uuid4)

    conversation_id: UUID

    role: str
    content: str

    created_at: datetime = Field(default_factory=utc_now)


class ConversationContext(BaseContract):
    conversation_id: UUID

    resolved_entities: list[EntityReference] = Field(
        default_factory=list
    )

    active_investigation_id: UUID | None = None

    context_summary: str | None = None

    updated_at: datetime = Field(default_factory=utc_now)