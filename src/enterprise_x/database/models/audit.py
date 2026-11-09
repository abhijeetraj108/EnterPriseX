import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from enterprise_x.database.base import Base


class AuditEvent(Base):

    __tablename__ = "audit_events"
    __table_args__ = (
        Index("ix_audit_entity", "entity_type", "entity_id"),
        Index("ix_audit_occurred_at", "occurred_at"),
        {"schema": "audit"},
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False
    )

    event_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    entity_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    entity_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    actor: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    event_data: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
        nullable=False
    )

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )